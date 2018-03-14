from django.db import models

# Create your models here.


class Area(models.Model):
    code = models.CharField(max_length=10, primary_key=True)

    def __str__(self):
        return self.code


class Location(models.Model):
    post_code = models.CharField(max_length=10, primary_key=True)
    post_code_structured = models.CharField(max_length=15)
    post_code_area = models.ForeignKey(Area, on_delete=models.PROTECT)
    SFBB_avail = models.FloatField(null=True)
    UFBB_avail = models.FloatField(null=True)
    NGA_avail = models.FloatField(null=True)
    perc_prem_not_2Mb = models.FloatField(null=True)
    perc_prem_not_5Mb = models.FloatField(null=True)
    perc_prem_not_10Mb = models.FloatField(null=True)
    perc_prem_not_30Mb = models.FloatField(null=True)
    median_dl_speed = models.FloatField(null=True)
    average_dl_speed = models.FloatField(null=True)
    min_dl_speed = models.FloatField(null=True)
    max_dl_speed = models.FloatField(null=True)
    average_dl_speed_less_10Mb = models.FloatField(null=True)
    average_dl_speed_BBB = models.FloatField(null=True)
    average_dl_speed_SFBB = models.FloatField(null=True)
    average_dl_speed_UFBB = models.FloatField(null=True)
    median_ul_speed = models.FloatField(null=True)
    average_ul_speed = models.FloatField(null=True)
    min_ul_speed = models.FloatField(null=True)
    max_ul_speed = models.FloatField(null=True)
    average_ul_speed_less_10Mb = models.FloatField(null=True)
    average_ul_speed_BBB = models.FloatField(null=True)
    average_ul_speed_SFBB = models.FloatField(null=True)
    average_ul_speed_UFBB = models.FloatField(null=True)
    average_data_usage = models.FloatField(null=True)
    average_data_usage_less_10Mb = models.FloatField(null=True)
    average_data_usage_BBB = models.FloatField(null=True)
    average_data_usage_SFBB = models.FloatField(null=True)
    average_data_usage_UFBB = models.FloatField(null=True)

    @classmethod
    def create_location(cls, fields):
        '''
        :param fields: dict of field names and their values
        :return: Location instance
        '''
        return cls(**fields)

    def __str__(self):
        return self.post_code_structured

