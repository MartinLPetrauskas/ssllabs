#!/usr/bin/env python3

import requests
import time
import sys
import logging

API = 'https://api.ssllabs.com/api/v3/'


def requestAPI(path, payload=None):
    """
    This is a helper function that takes the path to the relevant API call and the user defined payload and requests
    the data/server test from Qualys SSL Labs.
    @param path: path relevant to API call (usually 'analyze')
    @param payload: JSON object with information about the parameters for the API call
    @return: JSON object with results from API call
    """
    url = API + path

    try:
        response = requests.get(url, params=payload)
    except requests.exceptions.RequestException:
        logging.exception('Request failed.')
        sys.exit(1)

    data = response.json()
    return data


def scan(host, fromCache):
    """
    This function will begin an assessment and return the results
    @param host: hostname which will be analyzed
    @param fromCache: determines if the API will retrieve cached assessment reports
    @return: JSON object with API results
    """
    path = 'analyze'
    payload = {
        'host': host,
        'all': 'done',
        'ignoreMismatch': 'on',
    }
    if fromCache:
        payload.update({'fromCache': 'on', 'maxAge': 24})
    else:
        payload.update({'startNew': 'on'})
    results = requestAPI(path, payload)

    if not fromCache:
        payload.pop('startNew')

    # There is no need to poll for the results right away since it takes 60+ seconds to get them
    time.sleep(10)

    # A variety of errors can appear while making API requests.
    # Fail-safe option is to return if any errors appear and let the invoking program deal with them
    if 'errors' in results.keys():
        return results

    while results['status'] != 'READY' and results['status'] != 'ERROR':
        time.sleep(30)
        results = requestAPI(path, payload)

    return results


def resultsFromCache(host, publish='off', startNew='off', fromCache='on', all='done'):
    """
    This function will return cached assessment reports if they are available
    @param host: hostname which will be analyzed
    @param publish: on/off determines if the assessment results should be published on the public results boards
    @param startNew: on/off determines if the API will start a new assessment
    @param fromCache: on/off determines if the API will retrieve cached assessment reports
    @param all: on/done determines when the API returns the results
    @return: JSON object with results from API call
    """
    path = 'analyze'
    payload = {
                'host': host,
                'publish': publish,
                'startNew': startNew,
                'fromCache': fromCache,
                'all': all
              }
    data = requestAPI(path, payload)

    # There is no need to poll for the results right away since it takes 60+ seconds to get them
    time.sleep(10)

    # A variety of errors can appear while making API requests.
    # Fail-safe option is to return if any errors appear and let the invoking program deal with them
    if 'errors' in data.keys():
        return data

    while data['status'] != 'READY' and data['status'] != 'ERROR':
        time.sleep(30)
        data = requestAPI(path, payload)

    return data


def newScan(host, publish='off', startNew='on', all='done', ignoreMismatch='on'):
    """
    This function will begin a new assessment and return the results
    @param host: hostname which will be analyzed
    @param publish: on/off determines if the assessment results should be published on the public result boards
    @param startNew: on/off determines if the API will start a new assessment
    @param all: on/done determines when the API returns results
    @param ignoreMismatch: on/off determines how the API will proceed when the server certificate does not match the
    assessment hostname
    @return: JSON object with results from API call
    """
    path = 'analyze'
    payload = {
                'host': host,
                'publish': publish,
                'startNew': startNew,
                'all': all,
                'ignoreMismatch': ignoreMismatch
              }
    results = requestAPI(path, payload)

    payload.pop('startNew')

    # There is no need to poll for the results right away since it takes 60+ seconds to get them
    time.sleep(10)

    # A variety of errors can appear while making API requests.
    # Fail-safe option is to return if any errors appear and let the invoking program deal with them
    if 'errors' in results.keys():
        return results

    while results['status'] != 'READY' and results['status'] != 'ERROR':
        time.sleep(30)
        results = requestAPI(path, payload)

    return results
