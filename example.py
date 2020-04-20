#! /usr/bin/env python3

# Import the module
import ssllabsscanner

# To get results from cache, call resultsFromCache()
cache_data = ssllabsscanner.resultsFromCache("www.qualys.com")
print(cache_data['endpoints'][0]['grade'])

# To get fresh results, call newScan()
new_data = ssllabsscanner.newScan("www.qualys.com")
print(new_data['endpoints'][0]['grade'])
