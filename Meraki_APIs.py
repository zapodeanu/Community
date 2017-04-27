# developed by Gabi Zapodeanu, TSA, GSS, Cisco Systems

# !/usr/bin/env python3

import requests
import json

import requests.packages.urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from Meraki_APIs_init import MERAKI_API_KEY, MERAKI_URL, MERAKI_NETWORK_NAME

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings

# these variables need to change for your environment:
# the API key in the Meraki_APIs_init.py file
# the MERAKI_NETWORK_NAME in the Meraki_APIs_init.py


def pprint(json_data):
    """
    Pretty print JSON formatted data
    :param json_data:
    :return:
    """

    print(json.dumps(json_data, indent=4, separators=(' , ', ' : ')))


def meraki_get_organizations():
    """
    This function will get the Meraki Organization Id's and names the user has access to
    API call to /organizations
    :return: Meraki Organization Ids and names the user has access to
    """
    url = MERAKI_URL + '/organizations'
    header = {'content-type': 'application/json', 'X-Cisco-Meraki-API-Key': MERAKI_API_KEY}
    org_response = requests.get(url, headers=header, verify=False)
    org_json = org_response.json()
    pprint(org_json)
    org_list = []
    for org in org_json:
        org_info = [org['name'], org['id']]
        org_list.append(org_info)
    return org_list


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

    # we will return just one network, the first in the list of networks
    # we could return all the network ids by creating a List of ids

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


def main():

    # get the Meraki organization id

    meraki_organization_ids = meraki_get_organizations()
    print('\nYour Meraki Organization IDs and names are: ')
    pprint(meraki_organization_ids)

    # select the network id for the Network Name - MERAKI_NETWORK_NAME = 'Meraki Live Demo'

    for network in meraki_organization_ids:
        if network[0] == MERAKI_NETWORK_NAME:
            meraki_org_id = network[1]

    print('\nYour selected Meraki Organization Id is ', meraki_org_id)

    # get the Meraki networks info

    meraki_network_info = meraki_get_networks(meraki_org_id)
    meraki_network_id = meraki_network_info[0]

    # print the selected Meraki network info

    print('Your Meraki Network ID is: ', meraki_network_id)
    print('Your Meraki Network Name is: ', MERAKI_NETWORK_NAME)

    # get the Meraki Network Devices for a network

    meraki_devices_list = meraki_get_devices(meraki_network_id)
    print('\nYour Meraki Network Devices present in the network with the name ', MERAKI_NETWORK_NAME, ' : ')

    pprint(meraki_devices_list[0])  # sample of what info is provided for each network device

    # get the Meraki SM devices

    meraki_sm_devices_list = meraki_get_sm_devices(meraki_network_id)
    print('Your Meraki SM Devices list: \n')
    pprint(meraki_sm_devices_list[0])  # print the info from SM for one device


if __name__ == '__main__':
    main()
