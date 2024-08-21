#!/usr/bin/env python3

import os
import sys
import csv



mitigations= [
    "CONFIG_MITIGATION_PAGE_TABLE_ISOLATION",
    "CONFIG_MITIGATION_RETPOLINE",
    "CONFIG_MITIGATION_RETHUNK",
    "CONFIG_MITIGATION_UNRET_ENTRY",
    "CONFIG_MITIGATION_CALL_DEPTH_TRACKING",
    "CONFIG_MITIGATION_IBPB_ENTRY",
    "CONFIG_MITIGATION_IBRS_ENTRY",
    "CONFIG_MITIGATION_SRSO",
    "CONFIG_MITIGATION_SLS",
    "CONFIG_MITIGATION_GDS",
    "CONFIG_MITIGATION_RFDS",
    "CONFIG_MITIGATION_SPECTRE_BHI",
    "CONFIG_MITIGATION_MDS",
    "CONFIG_MITIGATION_TAA",
    "CONFIG_MITIGATION_MMIO_STALE_DATA",
    "CONFIG_MITIGATION_L1TF",
    "CONFIG_MITIGATION_RETBLEED",
    "CONFIG_MITIGATION_SPECTRE_V1",
    "CONFIG_MITIGATION_SPECTRE_V2",
    "CONFIG_MITIGATION_SRBDS",
    "CONFIG_MITIGATION_SSB"
]

def parse_output():
    ret = []
    entry = read_config()
    with open("results.log", 'r') as f:
        for line in f.readlines():
            if line.startswith("real"):
                continue
            elif line.startswith("bench_"):
                print(line)
                entry["bench"] = line.strip()
            elif line.startswith("average"):
                slices = line.split()
                entry["real"] = float(slices[2])
                entry['user'] = float(slices[4])
                entry['system'] = float(slices[6])

                ret.append(entry)
                entry = read_config()

    return ret


def read_config():
    entry = {}
    with open("/tmp/config", 'r') as f:
        lines = f.readlines()
        for mitigation in mitigations:
            entry[mitigation] = 'n'
            for line in lines:
                if f"{mitigation}=y" in line:
                    entry[mitigation] = 'y'

    entry["mitigations"] = ""
    with open("/proc/cmdline", 'r') as f:
        lines =  f.readlines()
        for line in lines:
            if "mitigations=off" in line:
                entry["mitigations"] = "off"

    return entry


# starts here
os.system("zcat /proc/config.gz | grep CONFIG_MITIGATION > /tmp/config")
entries = parse_output()
for data in entries:
    for k in reversed(data.keys()):
        print(f"{k},", end="")
    break

print()
for data in entries:
    for k in reversed(data.keys()):
        print(f"{data[k]},", end="")

    print("")
