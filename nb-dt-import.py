#!/usr/bin/env python3
from collections import Counter
from datetime import datetime
import yaml
import pynetbox
from glob import glob
import os
import sys
import time

import settings
from netbox_api import NetBox


def main():
    startTime = datetime.now()
    args = settings.args

    netbox = NetBox(settings)
    settings.handle.log("-=-=-=-=- Starting operation -=-=-=-=-")
    files, vendors = settings.dtl_repo.get_devices(
        f'{settings.dtl_repo.repo_path}/device-types/', args.vendors)

    settings.handle.log(f'{len(vendors)} Vendors Found')
    device_types = settings.dtl_repo.parse_files(files, slugs=args.slugs)
    settings.handle.log(f'{len(device_types)} Device-Types Found')
    settings.handle.log("Creating Manufacturers")
    netbox.create_manufacturers(vendors)
    settings.handle.log("Creating Device Types")
    netbox.create_device_types(device_types)

    settings.handle.log("-=-=-=-=- Checking Modules -=-=-=-=-")
    if netbox.modules:
        settings.handle.log("Modules Enabled. Creating Modules...")
        files, vendors = settings.dtl_repo.get_devices(
            f'{settings.dtl_repo.repo_path}/module-types/', args.vendors)
        settings.handle.log(f'{len(vendors)} Module Vendors Found')
        module_types = settings.dtl_repo.parse_files(files, slugs=args.slugs)
        settings.handle.log(f'{len(module_types)} Module-Types Found')
        netbox.create_manufacturers(vendors)
        netbox.create_module_types(module_types)

    settings.handle.log('---')
    settings.handle.verbose_log(
        f'Script took {(datetime.now() - startTime)} to run')
    settings.handle.log(f'{netbox.counter["added"]} devices created')
    settings.handle.log(f'{netbox.counter["images"]} images uploaded')
    settings.handle.log(f'{netbox.counter["updated"]} interfaces/ports updated')
    settings.handle.log(f'{netbox.counter["manufacturer"]} manufacturers created')
    if settings.NETBOX_FEATURES['modules']:
        settings.handle.log(f'{netbox.counter["module_added"]} modules created')
        settings.handle.log(f'{netbox.counter["module_port_added"]} module interface / ports created')
    
    settings.handle.log(f'{netbox.counter["connection_errors"]} connection errors corrected')
    settings.handle.log("-=-=-=-=- Ending operation -=-=-=-=-")
    time.sleep(5)

    # Uncomment the line below while troubleshooting to pause on completion
    #input("Debug pausing to review output. Press RETURN to close.")

def myexcepthook(type, value, traceback, oldhook=sys.excepthook):
    oldhook(type, value, traceback)
    input("Uncaught exception found. Press RETURN to continue execution.")

if __name__ == "__main__":
    # Uncomment the line below while troubleshooting to pause on uncaught exceptions
    #sys.excepthook = myexcepthook
    main()
