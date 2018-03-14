from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import *
from django.views.decorators.csrf import csrf_exempt
import pyspeedtest
import statistics


def run_local_speed_test():
    st = pyspeedtest.SpeedTest()
    return twodp(st.download() / (1024 * 1024)), twodp(st.upload() / (1024 * 1024)), twodp(st.ping())


def error_message(message):
    error = {'error': message}
    return JsonResponse(error, safe=False)


def twodp(val):
    return float("{0:.2f}".format(val))


@csrf_exempt
def start_view(request):
    if request.method == 'GET':
        return render(request, 'search.html', dict())

    elif request.method == 'POST' and request.is_ajax():
        pc = request.POST['p_code']
        pc = "".join(pc.split())
        pc = pc.upper()
        area_code = pc[:2]
        context = dict()

        # find area for postcode
        try:
            area = Area.objects.get(code=area_code)
            context['area_code'] = area_code
            print('Area "{}" found'.format(area_code))
        except Area.DoesNotExist:
            print('Could not find area "{}"'.format(area_code))
            return error_message('Could not find a Post Code Area matching %s' % area_code)

        # find location
        try:
            loc = Location.objects.get(post_code=pc)
            context['loc'] = loc
            print('Found location "{}"'.format(pc))
        except Location.DoesNotExist:
            print('Could not find a location for "{}"'.format(pc))

        # find area locations
        area_locs = Location.objects.filter(post_code_area__code=area).values()
        if not area_locs:
            return error_message('Could not find any Locations matching {}'.format(area_code))
        print('{} locations for area code "{}"'.format(len(area_locs), area_code))

        # aggregate
        field_names = [k for k, v in area_locs[0].items() if 'post_code' not in k]
        loc_data_lists = dict()
        for l in area_locs:
            for k, v in l.items():
                if k in field_names:
                    if k not in loc_data_lists:
                        loc_data_lists[k] = []
                    loc_data_lists[k].append(v)

        for k, v in loc_data_lists.items():
            v = [x for x in v if x not in [None, 'NULL', '']]
            if 'median' in k:
                context[k] = twodp(statistics.median(v))
            elif 'min' in k:
                context[k] = twodp(min(v))
            elif 'max' in k:
                context[k] = twodp(max(v))
            else:
                context[k] = twodp(statistics.mean(v))

        context['user_download'], context['user_upload'], context['user_ping'] = run_local_speed_test()

        template = render_to_string('results.html', context, request)

        return JsonResponse({'results': template}, safe=False)

    else:
        return render(request, 'search.html', dict())





