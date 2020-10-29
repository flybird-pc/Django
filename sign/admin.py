from django.contrib import admin

from sign.models import Event,Guest

# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ['id','create_time','name','limit','status','address','start_time']
    search_fields = ['name'] #搜索栏
    list_filter = ['status'] #过滤器

class GuestAdmin(admin.ModelAdmin):
    list_display = ['event_id','create_time','real_name','phone','email','sign']


admin.site.register(Event,EventAdmin)
admin.site.register(Guest,GuestAdmin)
