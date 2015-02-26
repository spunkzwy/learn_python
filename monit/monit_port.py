import socket
import threading
import time
import struct
import Queue

queue = Queue.Queue()

def udp_sender(ip,port):
    '''
    send udp package
    '''
    try:
        ADDR = (ip,port)
        sock_udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        sock_udp.sendto("abcd...",ADDR)
        sock_udp.close()
    except:
        pass

def icmp_receiver(ip,port):
    '''
    receive icmp package,Determine the udp port state
    '''
    icmp = socket.getprotobyname("icmp")
    try:
        sock_icmp = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    except socket.error, (errno, msg):
        if errno == 1:
            # Operation not permitted
            msg = msg + (
                " - Note that ICMP messages can only be sent from processes"
                " running as root."
            )
            raise socket.error(msg)
        raise # raise the original error
    sock_icmp.settimeout(3)
    try:
        recPacket,addr = sock_icmp.recvfrom(64)
    except:
        queue.put(True)
        return
    icmpHeader = recPacket[20:28]
    icmpPort = int(recPacket.encode('hex')[100:104],16)
    head_type, code, checksum, packetID, sequence = struct.unpack(
            "bbHHh", icmpHeader
    )
    sock_icmp.close()
    if code == 3 and icmpPort == port and addr[0] == ip:
        queue.put(False)
    return

def check_udp(ip,port):
    ''' 
    Check the udp port state,
    If the port is open,return True
    If the port is down,resturn False
    '''

    thread_udp = threading.Thread(target=udp_sender,args=(ip,port))
    thread_icmp = threading.Thread(target=icmp_receiver,args=(ip,port))

    thread_udp.daemon= True
    thread_icmp.daemon = True

    thread_icmp.start()
    time.sleep(0.1)
    thread_udp.start()

    thread_icmp.join()
    thread_udp.join()
    return queue.get()

def check_tcp(host,port):
    ''' 
       Check the tcp port state,
       If the port is open,return True
       If the port is down,resturn False
    '''
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:   
        sock.connect((host,port))
        sock.close()
        return True
    except Exception:
        return False
