from django.db.models.query import QuerySet
from decimal import Decimal
from datetime import datetime
import pytz
import iso8601


def localizeTime(dateStr, fmt = None):
	if dateStr == 'None':
		return dateStr
	if fmt == None:
		fmt = "%Y-%m-%d %H:%M:%S"
	ist = pytz.timezone('Asia/Kolkata')
	d = iso8601.parse_date(dateStr)
	d = d.astimezone(ist)
	d =  d.strftime(fmt)
	return d

def QuerySetSerializer(queryset, req_fields = [], skip_fields = [], name_key_dict = None):
	
	'''
	A common serializer to serializer django QuerySet of any django model
	
	queryset        :- Django QuerySet object to serialize
	
	req_fields      :- Array of models field name that needs to be serialized.
						if req_fields is [] or not provided during function call
							then it will serialize (all fields of model - skip_fields)
						otherwise (req_fields - skip_fields) will be serialized

	skip_fields     :- Name of fields that will not be serialized or that will be skipped.
	
	name_key_dict   :- Name key dictionary will have maping of field name of the model and
					   and key of the field in JSON
					   if a particular field do not have any entry in name_key_dict then model 
						field name will be key of JSON
	'''
	
	data = []
	if isinstance(queryset, QuerySet) and bool(queryset):
		modelType = type(queryset.first()) # Getting model class type 
		allowed_fields = []

		'''Iterating over all the field of the model to find out allowed field for JSON'''
		
		for field in modelType._meta.fields:
			
			'''Getting field name, Using attname instead of name as it gives 
					ForeignKey field name with _id'''
			
			fieldName = field.attname
			
			'''Ignore field if it is in skip_fields'''
			
			if fieldName in skip_fields:
				continue
			
			'''If req_fields is non empty and field in req_fields then append to allowed_fields'''

			elif req_fields and fieldName in req_fields:
				allowed_fields.append(fieldName)            
			
			else :
				allowed_fields.append(fieldName)
		
		for obj in queryset :
			item = {}
			for field in allowed_fields:
				
				'''If field name is in name_key_dict then use it value as key to JSON
						othewise use field name as key'''
				
				if name_key_dict and name_key_dict.get(field):
					key_name = name_key_dict.get(field)
				else :
					key_name = field
				
				value = getattr(obj, field)
				if isinstance(value, Decimal): # If Decimal the convert to string
					item[key_name] = str(value)
				elif isinstance(value, datetime): # Localize the time for datetime object
					item[key_name] = localizeTime(str(value))
				else :
					item[key_name] = value
			
			data.append(item)
	
	return data
