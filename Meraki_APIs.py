# developed by Gabi Zapodeanu, TSA, GSS, Cisco Systems

# !/usr/bin/env python3

import requests
import json

import requests.packages.urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from Meraki_APIs_init import MERAKI_API_KEY, MERAKI_CUSTOMER_NUMBER, MERAKI_URL

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings



def pprint(json_data):
    """
    Pretty print JSON formatted data
    :param json_data:
    :return:
    """

    print(json.dumps(json_data, indent=4, separators=(' , ', ' : ')))



def meraki_get_organizations():
    """
    This function will get the Meraki Organization Id
    API call to /organizations
    :return: Meraki Organization Id
    """
    url = MERAKI_URL + '/organizations'
    header = {'content-type': 'application/json', 'X-Cisco-Meraki-API-Key': MERAKI_API_KEY}
    org_response = requests.get(url, headers=header, verify=False)
    org_json = org_response.json()
    org_id = org_json[0]['id']
    return org_id


def meraki_get_networks(organization_id):
    """
    This function will return the list of networks associated with the Meraki Organization ID
    API call to /organizations/{organization_id]/networks
    :param organization_id: Meraki Organization ID
    :return: network ids and names
    """
    url = MERAKI_URL + '/organizations/' + str(organization_id) + '/networks'
    header = {'content-type': 'application/json', 'X-Cisco-Meraki-API-Key': MERAKI_API_KEY}
    networks_response = requests.get(url, headers=header, verify=False)
    networks_json = networks_response.json()
    network_id = networks_json[0]['id']
    network_name = networks_json[0]['name']
    return network_id, network_name


def meraki_get_sm_devices(network_id):
    """
    This function will return the list of networks associated with the Meraki Network ID
    API call to /networks/{organization_id]/sm/devices
    :param network_id: Meraki network ID
    :return: list with all the SM devices
    """

    url = MERAKI_URL + '/networks/' + str(network_id) + '/sm/devices?fields=phoneNumber,location'
    header = {'content-type': 'application/json', 'X-Cisco-Meraki-API-Key': MERAKI_API_KEY}
    sm_devices_response = requests.get(url, headers=header, verify=False)
    sm_devices_json = sm_devices_response.json()['devices']
    return sm_devices_json


def meraki_get_devices(network_id):
    """
    This function will return a list with all the network devices associated with the Meraki Network Id
    :param network_id: Meraki Network ID
    :return: list with all the devices
    """
    url = MERAKI_URL + '/networks/' + str(network_id) + '/devices'
    header = {'content-type': 'application/json', 'X-Cisco-Meraki-API-Key': MERAKI_API_KEY}
    devices_response = requests.get(url, headers=header, verify=False)
    devices_json = devices_response.json()
    return devices_json


def meraki_get_ssids(network_id):
    """
    This function will return the Meraki Network id list of configured SSIDs
    :param network_id: Meraki Network id
    :return: list of SSIDs
    """
    url = MERAKI_URL + '/networks/' + str(network_id) + '/ssids'
    header = {'content-type': 'application/json', 'X-Cisco-Meraki-API-Key': MERAKI_API_KEY}
    ssids_response = requests.get(url, headers=header, verify=False)
    ssids_json = ssids_response.json()

    # filter only configured SSIDs
    ssids_list = []
    for ssid in ssids_json:
        if 'Unconfigured' not in ssid['name']:
            ssids_list.append(ssid)
    return ssids_list



def main():


    # get the Meraki organization id

    meraki_org_id = meraki_get_organizations()
    print('\nYour Meraki Organization ID is: ', meraki_org_id)

    # get the Meraki networks info

    meraki_network_info = meraki_get_networks(meraki_org_id)
    # meraki_network_id = meraki_network_info[0]
    # meraki_network_name = meraki_network_info[1]

    # print('Your Meraki Network ID is: ', meraki_network_id)
    # print('Your Meraki Network Name is: ', meraki_network_name)

    # get the Meraki Network Devices

    # meraki_devices_list = meraki_get_devices(meraki_network_id)
    # print('\nYour Meraki Network Devices are: ')
    # pprint(meraki_devices_list)

    # get the Meraki SM devices

    #meraki_sm_devices_list = meraki_get_sm_devices(meraki_network_id)
    #print('Your Meraki SM Devices list: \n')
    #pprint(meraki_sm_devices_list)



if __name__ == '__main__':
    main()
