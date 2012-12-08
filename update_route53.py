#!/usr/bin/env python
#
# Updates the A record on AWS Route53 with your current IP address

import requests
import boto
from boto.route53.record import ResourceRecordSets
 
# Obligatory config stuff
zone_id = '' # The zone ID from Route53 eg ZXXXXXXXXXXXXX
zone_domain = '' # eg foo.bar.org

# Find out our current external IPv4 address
r = requests.get(r'http://jsonip.com')
ip = r.json['ip']

# Update the A record on Route53
conn = boto.connect_route53()
changes = ResourceRecordSets(conn, zone_id)
response = conn.get_all_rrsets(zone_id, 'A', zone_domain, maxitems=1)[0]
change1 = changes.add_change("DELETE", zone_domain, 'A', response.ttl)
for old_value in response.resource_records:
    change1.add_value(old_value)
change2 = changes.add_change("CREATE", zone_domain, 'A', 600)
change2.add_value(ip)
changes.commit()