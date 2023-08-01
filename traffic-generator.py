import requests
from faker import Faker
from dataclasses import dataclass, field
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP
from scapy.utils import wrpcap

VALID_METHODS = ['GET', 'POST', 'PUT', 'DELETE']
STATUS_CODES = [200, 201, 204, 400, 404, 500]


@dataclass
class Traffic:

    url: str = field(init=False)
    method: str = field(init=False)
    user_agent: str = field(init=False)
    source_ip: str = field(init=False)
    destination_ip: str = field(init=False)
    status_code: int = field(init=False)
    content_length: int = field(init=False)

    def to_pcap(self):

        http_request = (
                Ether()
                / IP(src=self.source_ip, dst=self.destination_ip)
                / TCP(dport=80, sport=12345)
                / f"GET {self.url} HTTP/1.1\r\nHost: {self.source_ip}\r\nUser-Agent: {self.user_agent}\r\n\r\n"
        )
        wrpcap(filename=self.source_ip.pcap, pkt=http_request)


class TrafficGenerator:
    def __init__(self):
        self.faker = Faker()
        self.traffics: list[Traffic] = []

    def generate_traffic_item(self):
        traffic = Traffic()
        traffic.url = self.faker.url()
        traffic.method = self.faker.random_element(VALID_METHODS)
        traffic.user_agent = self.faker.user_agent()
        traffic.source_ip = self.faker.ipv4()
        traffic.destination_ip = self.faker.ipv4()
        traffic.status_code = self.faker.random_element(STATUS_CODES)
        traffic.content_length = self.faker.random_int(min=100, max=1000)
        self.traffics.append(traffic)

    def run(self, iterations):
        for _ in range(iterations):
            self.generate_traffic_item()
        [print(traffic) for traffic in self.traffics]

        # for traffic in self.traffics:
            # traffic.to_pcap()


traffic_gen = TrafficGenerator()
traffic_gen.run(4524)






