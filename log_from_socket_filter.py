from docker import Client
import socket
import json
from threading import Thread
from time import sleep

c_list = []

def print_logs(container, stream, historical_log=False):
    g = c.attach(container=container["Id"], stdout=True, stream=True, stderr=True, logs=historical_log)
    for line in g:
        print line
        stream.send(line)

    callback(container)

def callback(container):
    print "Stop monitor log for container: {0}".format(container["Id"])
    c_list.remove(container)


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 1514
    while True:
        try:
            s.connect((host,port))
            if s.getpeername():
                print "Connected to {0}".format(s.getpeername())
                break
        except:
            print "Port 1514 is not ready, sleep for a moment"
            sleep(3)

    c = Client(base_url='unix://var/run/docker.sock')

    while True:
        run_c_list = c.containers()

        for container in run_c_list:
            container_found = False
            for existing_container in c_list:
                if container["Id"] == existing_container["Id"]:
                        container_found = True
                        break

            if container_found == False:
                if "Labels" in container and "io.kubernetes.pod.namespace" in container["Labels"]:
                    if container["Labels"]["io.kubernetes.pod.namespace"] != "kube-system":
                        #print json.dumps(container,indent=2)
                        c_list.append(container)
                        print "Monitor log for new container : {0}".format(container["Id"])
                        thread = Thread(target = print_logs, args = (container,s,))
                        thread.start()

        sleep(3)
        print "Total number of containers monitored {0}".format(len(c_list))
        if len(c_list) == 0:
            print "Zero containers running, self kill"
            break
