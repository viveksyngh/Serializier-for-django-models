from django.db.models.query import QuerySet
from VendorApp.models import Vendor, OrgVendorBalance
from decimal import Decimal
from datetime import datetime

def QuerySetSerializer(queryset, req_fields = [], skip_fields = [], name_map_dict = None):
    data = []
    if isinstance(queryset, QuerySet) and bool(queryset):
        modelType = type(queryset.first())
        allowed_field = []
        for field in modelType._meta.fields :
            if field.name in skip_fields:
                continue
            elif req_fields and field.name in req_fields:
                allowed_field.append(field.name)
            else :
                allowed_field.append(field.name)
        for obj in queryset :
            item = {}
            for field in allowed_field:
                if name_map_dict and name_map_dict.get(field):
                    key_name = name_map_dict.get(field)
                else :
                    key_name = field
                print type(getattr(obj, field))
                item[key_name] = getattr(obj, field)
            data.append(item)    
    return data

def test():
    vendors = Vendor.objects.all().filter(orgId = 'VATechVentures')
    #vendorBalances = OrgVendorBalance.objects.all()
    #VendorSlice = vendors[:10]
    #print QuerySetSerializer(vendorBalances)
    print QuerySetSerializer(vendors)

