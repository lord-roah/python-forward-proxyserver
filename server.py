import sys
import socket
import os
import ssl
import threading
import errno
import random

def string_capture(point1,point2,searchstring):
    pos1=searchstring.find(point1)+ len(point1)
    pos2=searchstring.find(point2)
    captured=searchstring[pos1:pos2]
    return captured


buffer_size=8192
proxy_list=[('101.255.82.66',80),('150.138.201.2',8080),('83.142.160.6',3128),('91.211.112.248',8080),('46.97.103.50',3128)]
alive_proxies=[]
dead_proxies=[]
smooth_chain=[]
https_proxy_list=[]






server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

serverip='0.0.0.0'
serverport=8777
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.bind((serverip,serverport))
server.listen(5)
print("[*]server online...")


def handle_client(conn,addr):

    request=conn.recv(buffer_size)
    op=request.split('\n')[0]

    first=string_capture('://','HTTP',op)
    second=string_capture('','/',first)
    third=second.find(':')
    if third == -1:
        port=443
        webserver=second
    else:
        hos,p=second.split(':',1)
        port=p
        webserver=hos
    proxyserver(conn,request,webserver,port,addr)







def proxyserver(con,data,webserver,port,addr):
 try:
    proxy=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ssl_proxy=ssl.wrap_socket(proxy)

    ip=str(socket.gethostbyname(webserver))
    host_name=webserver


    ssl_proxy.connect((webserver,port))

    ssl_proxy.send(data)

    while 1:
        reply=proxy.recv(buffer_size)
        if(len(reply)> 0):
            con.send(reply)

            print "[+]processed request from: %s:%d to %s(%s)\n" %(addr[0],addr[1],host_name,ip)
            #log= "[+]processed request from: %s:%d to %s(%s)\n" %(addr[0],addr[1],host_name,ip)
            #os.chdir('/home/k1ng')
            #log_file=open('log.txt','a')
            #log_file.write(log)
            #log_file.close()
        else:
            break
    ssl_proxy.close()
    con.close()
 except socket.error as e:
     if e.errno !=10054:
         print e
     else:
         pass


def proxy_tester(proxy_list):
    p=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    for proxy in proxy_list:

        value=p.connect_ex(proxy)
        if (value == 0):
            alive_proxies.append(proxy)
            p.close()

        else:
            dead_proxies.append(proxy)
            p.close




while True:
 try:
    connc,addr=server.accept()

    client_thread=threading.Thread(target=handle_client,args=(connc,addr))
    print connc,addr
    client_thread.start()
 except KeyboardInterrupt:
     server.close()
     print "[*]proxy server goin offline....."
     print "[*]good;;..bye babe..."
     sys.exit(1)
