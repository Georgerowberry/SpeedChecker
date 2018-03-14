import pandas as pd
import sqlite3
import os
import sys
from django.apps import apps
import django


def main():

    location = apps.get_model('Checker', 'Location')
    area = apps.get_model('Checker', 'Area')

    directory = '../SpeedChecker/Data'

    for filename in os.listdir(directory):
        data = pd.read_csv(directory+'/'+filename)

        # add area codes
        area_codes = sorted(set(data['postcode area'].tolist()))
        for a in area_codes:
            ar = area(a)
            ar.save()

        print('Adding {} area codes and {} locations'.format(len(area_codes), len(data)))

        data = data.applymap(lambda x: None if x == 'N/A' else x)
        rename_dict = {data.columns[0]: 'post_code',
                       data.columns[1]: 'post_code_structured',
                       data.columns[2]: 'post_code_area_id',
                       data.columns[3]: 'SFBB_avail',
                       data.columns[4]: 'UFBB_avail',
                       data.columns[5]: 'NGA_avail',
                       data.columns[6]: 'perc_prem_not_2Mb',
                       data.columns[7]: 'perc_prem_not_5Mb',
                       data.columns[8]: 'perc_prem_not_10Mb',
                       data.columns[9]: 'perc_prem_not_30Mb',
                       data.columns[10]: 'median_dl_speed',
                       data.columns[11]: 'average_dl_speed',
                       data.columns[12]: 'min_dl_speed',
                       data.columns[13]: 'max_dl_speed',
                       data.columns[14]: 'average_dl_speed_less_10Mb',
                       data.columns[15]: 'average_dl_speed_BBB',
                       data.columns[16]: 'average_dl_speed_SFBB',
                       data.columns[17]: 'average_dl_speed_UFBB',
                       data.columns[18]: 'median_ul_speed',
                       data.columns[19]: 'average_ul_speed',
                       data.columns[20]: 'min_ul_speed',
                       data.columns[21]: 'max_ul_speed',
                       data.columns[22]: 'average_ul_speed_less_10Mb',
                       data.columns[23]: 'average_ul_speed_BBB',
                       data.columns[24]: 'average_ul_speed_SFBB',
                       data.columns[25]: 'average_ul_speed_UFBB',
                       data.columns[32]: 'average_data_usage',
                       data.columns[33]: 'average_data_usage_less_10Mb',
                       data.columns[34]: 'average_data_usage_BBB',
                       data.columns[35]: 'average_data_usage_SFBB',
                       data.columns[36]: 'average_data_usage_UFBB',
                       }

        data = data.rename(columns=rename_dict)
        data = data.where((pd.notnull(data)), '')
        field_names = [v for k, v in rename_dict.items()]
        sql_fields = ', '.join(['"'+x+'"' for x in field_names])
        con = sqlite3.connect('SpeedChecker/../db.sqlite3')
        cur = con.cursor()
        pos = 0
        count = 0
        for index, row in data.iterrows():
            values = ['"'+str(row[x])+'"' if str(row[x]) == row[x] else str(row[x]) for x in field_names]
            sql = "INSERT INTO Checker_location ({}) SELECT {} WHERE NOT EXISTS(SELECT 1 FROM Checker_location WHERE post_code = '{}');".format(
                sql_fields, ', '.join(values), row['post_code'])
            cur.execute(sql)
            pos += 1
            count += 1
            if pos == 50000:
                print('{} done'.format((count/len(data))*100))
                pos = 0

        print('finished loading {}'.format(filename))
        con.commit()
    print('Done!')


if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(BASE_DIR)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'SpeedChecker.settings'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SpeedChecker.settings')
    django.setup()
    main()
