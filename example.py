#! /usr/bin/env python3

# Import the module
import ssllabsscanner

# To get results from cache, call scan with fromCache parameter set to True
cache_data = ssllabsscanner.scan("www.qualys.com", True)
print(cache_data['endpoints'][0]['grade'])

# To get fresh results, call scan with fromCache parameter set to False
new_data = ssllabsscanner.scan("www.qualys.com", False)
print(new_data['endpoints'][0]['grade'])
