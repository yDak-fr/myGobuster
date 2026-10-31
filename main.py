import socket 
import ssl
import sys


CODES_3 = ["301","302","303","307","308"]


def http_or_https(host,protocol,path="/"):

    port = 80
    raw_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_soc.settimeout(10)
    soc = raw_soc

    code = ""

    if protocol == "https":

        port = 443
        
        context = ssl.create_default_context()
        tls_socket = context.wrap_socket(raw_soc,server_hostname=host)   #tls certyfikat, SNI i wymaina danymi z wersjami i szyfrowaniem 
        tls_socket.settimeout(10)

        soc = tls_socket

  
    soc.connect((host,port))


    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"HOST: {host}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )

    soc.send(request.encode())

    #---------------------------------------------------------------------------------------------

    response = ""
    while True:
        chunk = soc.recv(4096).decode()                 # pobranie danych od serwera ze strumienia
        if not chunk:
            break
        response += chunk

    #---------------------------------------------------------------------------------------------
    soc.close()

    #? print(response)
        
    response = response.split("\r\n")
    code = response[0][9:12]

    #---------------------------------------------------------------------------------------------

    if code in CODES_3:
        for line in response:
            if line.find("Location:") == 0:
                return (code,host,path,line[line.find(' ')+1:])


    return (code,host,path,"")

def start():

    check_input()

    main_name = sys.argv[1]

    list_of_directories = get_list_of_directories(sys.argv[2])

    main_graphic()

    for directory in list_of_directories:
        start_for_directory(main_name + '/' + directory.strip())


    main_graphic_end()

def start_for_directory(url):

    host,path,protocol = unwrap_message(url)
    code = ""
    new_redirect = ""

    og_path = path[:]


    while code == "" or code in CODES_3:

        try:
            code,host,path,new_redirect = http_or_https(host,protocol,path)
        except:
            one_directory_graphic(path,"ERROR")
            break


        if new_redirect:
            if if_new_redirect_is_whole_url(new_redirect):
                host,path,protocol = unwrap_message(new_redirect)
            else:
                path = new_redirect

        #print(code,host,path,new_redirect)

    one_directory_graphic(og_path,code)


def get_list_of_directories(path_worlist):

    list_of_directories = []
    file = open(path_worlist)

    list_of_directories = file.readlines()
    file.close()
    return list_of_directories
    

def unwrap_message(line_of_url):

    http = line_of_url.find("http://")
    https = line_of_url.find("https://")

    if http == -1 and https == -1:
        print("LACK OF HTTP OR HTTPS")
        exit(3)

    if line_of_url[-1] != '/':
        line_of_url += '/'

    host_path = line_of_url[line_of_url.find('/')+2:]

    path = host_path[host_path.find('/'):] 
    host = host_path[:host_path.find('/')]

    if http!=-1:
        protocol = 'http'
    else:
        protocol = 'https'


    return (host,path,protocol)


    

def check_input():
    if len(sys.argv)!= 3:
        print("BAD ORDER OR NUMBER OF ARGUMENTS")
        exit(2)



def if_new_redirect_is_whole_url(line) -> bool:
    if line[0] == '/':
        return False
    else:
        return True


def main_graphic():
    print('----------------------------------------')
    print('START SCANNING...')
    print('----------------------------------------')

def one_directory_graphic(path,code):
    print(f"{path} - {code}")

def main_graphic_end():
    print('----------------------------------------')
    

start()

#https("zsso-skierniewice.pl","/aha")

