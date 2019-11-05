import socks
import socket

from subprocess import getoutput as shell
from time import sleep


class Tor(object):

    def __init__(self):
        super(Tor, self).__init__()

    def restart_tor(self, num=3):
        shell('service tor restart')
        sleep(1.5)
        self.update_ip(num)

    @staticmethod
    def stop_tor():
        shell('service tor stop')

    def install_tor(self):
        self.connection()
        if not self.alive:
            return
        print('Installing Tor ...')
        shell('echo "deb http://http.kali.org/kali kali-rolling main contrib non-free" > /etc/apt/sources.list \
                                    && apt-get update && apt-get install tor -y && apt autoremove -y')

    def get_ip(self):
        try:
            ip = None
            br = self.create_browser()
            ip = br.open('https://api.ipify.org/?format=text', timeout=2).read()
            br.close()
        except Exception as e:
            print(e)
            pass
        finally:
            if not self.alive:
                self.exit()
            return ip

    def update_ip(self, recur=3):
        if not self.alive:
            self.exit()
        socks.socket.setdefaulttimeout(5)
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050, True)
        socket.socket = socks.socksocket

        try:
            ip = self.get_ip()
            if all([not ip, recur]):
                print('Error: Network unreachable')
                reset_counts = 2
                for _ in range(30):
                    if not self.alive:
                        return
                    ip = self.get_ip()
                    if ip:
                        break
                    else:
                        if reset_counts:
                            reset_counts -= 1
                            shell('service network-manager restart')
                        sleep(1)
                if not ip:
                    self.restart_tor(recur - 1)
            if all([not ip, not recur]):
                self.connection()

            if ip in self.recentIPs.queue:
                self.restart_tor()
            else:
                self.ip = ip
                self.recentIPs.put(ip)

        except Exception as e:
            print(e)
            pass
