from django import template

register = template.Library()


@register.filter
def humanise_bits(val):
    for unit in ['M', 'G']:
        if abs(val) < 1024.0:
            return "%3.1f%sb" % (val, unit)
        val /= 1024.0


@register.filter
def get_change(loc, area):
    return float("{0:.2f}".format(((loc - area) / area)*100))


@register.filter
def to_pos(val):
    return val * -1

