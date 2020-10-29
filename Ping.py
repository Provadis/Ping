import csv
import itertools
import subprocess
import concurrent.futures
import time

def csv_to_list(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        return list(reader)


def ping(ip):
    output = subprocess.run(['ping', ip], stdout=subprocess.PIPE)
    output = output.stdout.decode('cp437')
    ms = output[-18:].split(' ')[-1].strip().replace('ms', '')
    try:
        ms = int(ms)
    except:
        ms = -1
    return [ip, ms]


def get_IPs():
    IPs = csv_to_list('IPs.csv')
    IPs = list(itertools.chain.from_iterable(IPs))
    return IPs


def loop(IPs):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = [executor.submit(ping, ip) for ip in IPs]
    return results



if __name__ == '__main__':
    loop()
