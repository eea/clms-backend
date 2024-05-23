from zope.site.hooks import setSite
import json
import datetime
import DateTime
import csv
from clms.statstool.restapi.utils import (
    get_affiliation,
    get_country,
    get_sector_of_activity,
    get_thematic_activity,
)

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        elif isinstance(obj, DateTime.DateTime):
            return obj.ISO8601()
        return super(DateTimeEncoder, self).default(obj)


setSite(app.Plone)
mp = app.Plone.acl_users.mutable_properties

FIELDNAMES = ['affiliation', 'country', 'email', 'fullname', 'initial_login_time', 'last_login_time', 'sector_of_activity', 'thematic_activity', 'userid']

def decorate(dict_item):
    new_dict = {}
    for k,v in dict_item.items():
        if k in FIELDNAMES:
            if k == 'affiliation':
                new_dict[k] = get_affiliation(v)
            elif k == "country":
                new_dict[k] = get_country(v)
            elif k == "sector_of_activity":
                new_dict[k] = get_sector_of_activity(v)
            elif k == "thematic_activity":
                new_dict[k] = get_thematic_activity(v)
            else:
                new_dict[k] = v
    return new_dict


data = []
keys = mp._storage.keys()
for key in keys:
    values = mp._storage[key]
    values.update({'userid': key})
    if not values.get('isGroup', None):
        data.append(decorate(values))


with open('data.json', 'w') as fp:
    json.dump(data, fp, cls=DateTimeEncoder)

with open('data.csv', 'w') as fp:
    writer = csv.DictWriter(fp, fieldnames=FIELDNAMES)
    writer.writeheader()
    writer.writerows(data)
