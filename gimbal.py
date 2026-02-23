data = [
    "aa55060000474dff",
    "aa55100000c302055531303000000000c0ff",
    "aa55100000c3034142d1519e0000000019ff",
    "aa55100000c3034142d1519f000000001aff",
    "aa55100000c3034102d1519f00000000daff",
    "aa55100000c3034102e14d9f00000000e6ff",
    "aa55100000c3034142d1499f0000000012ff",
    "aa55100000c3034242c1499d0000000001ff",
    "aa55100000c30343c2d14999000000008eff",
    "aa55100000c30345c2f14d9300000000aeff",
    "aa55100000c3034843014d8b000000003aff",
    "aa55100000c3034b431151820000000048ff",
    "aa55100000c3034dc321517a00000000d2ff",
    "aa55100000c3035083315171000000009cff",
    "aa55100000c303540301416500000000d4ff",
    "aa55100000c30357c321455600000000acff",
    "aa55100000c3035c43314542000000002dff",
    "aa55100000c303608341512d0000000078ff",
    "aa55100000c3036483015d170000000032ff",
    "aa55100000c30367c2e175010000000056ff",
    "aa55060000474dff",
    "aa55100000c302055531303000000000c0ff",
]
data = [
    "aa55060000474dff",
    "aa550b0000916300000000ffff",
    "aa550b0000916ed60c0100edff",
    "aa550b0000916f000001000cff",
    "aa550b0000916e0e2c020046ff",
    "aa550b0000916ff700020004ff",
    "aa550b0000916e0b4a030062ff",
    "aa550b0000916f0800030016ff",
    "aa550b000091650100000103ff",
    "aa550b000091670000000003ff",
    "aa550b000091660100000003ff",
    "aa550b0000916300000000ffff",
    "aa550b0000916ed60c0100edff",
    "aa550b0000916f000001000cff",
    "aa550b0000916e0e2c020046ff",
    "aa550b0000916ff700020004ff",
    "aa550b0000916e0b4a030062ff",
]
import binascii
data = [binascii.unhexlify(d) for d in data]

# pip install bleak>=2.1.1

# Name: bleak
# Version: 2.1.1
# Summary: Bluetooth Low Energy platform Agnostic Klient
# Home-page: https://github.com/hbldh/bleak

from bleak import BleakScanner, BleakClient, BleakGATTCharacteristic

import asyncio
import struct
import uuid

class GimbalScanner(BleakScanner):
    SERVICE_UUID_FILTER = [f"0000{uid}-0000-1000-8000-00805f9b34fb" for uid in ["1800", "1801", "180a", "1812", "ae00", "ffe0"]]
    def __init__(self):
        super().__init__(service_uuids=GimbalScanner.SERVICE_UUID_FILTER)

class GimbalClient(BleakClient):   
    SERVICE_UUID = '0000ffe0-0000-1000-8000-00805f9b34fb'
    WRITE_CHARACTERISTIC = '0000ffe1-0000-1000-8000-00805f9b34fb'
    NOTIFY_CHARACTERISTIC = '0000ffe2-0000-1000-8000-00805f9b34fb'

    def __init__(self, ble_address):
        super().__init__(ble_address)

    def on_notify(self, sender: BleakGATTCharacteristic, data):
        print(f"{sender}: {data}")

    async def connect(self, **kwargs):
        await super().connect(**kwargs)
        await self.start_notify(GimbalClient.NOTIFY_CHARACTERISTIC, self.on_notify)
    
    async def disconnect(self, **kwargs):
        await self.stop_notify(GimbalClient.NOTIFY_CHARACTERISTIC)
        await super().disconnect(**kwargs)

    # async def read(self):
    #     resp = await self.read_gatt_char(READ_CHARACTERISTIC)
    #     return resp
    
    async def write(self, data):
        return await self.write_gatt_char(GimbalClient.WRITE_CHARACTERISTIC, data, response=True)


async def main(address = None):
    if address is None:
        print("BLE Scanning...")
        print()

        gimbal_devices = await GimbalScanner.discover()
        print(gimbal_devices)
        print()
        
        device = gimbal_devices[0]
        address = device.address
        print(f"BLE Device: {device.name}")
    
    print()
    print(f"BLE Address: {address}")

    async with GimbalClient(address) as gimbal:
        print(f"BLE connected: {gimbal.is_connected}")
        print()

        for d in data:
            await gimbal.write(d)
            # await asyncio.sleep(0.5)
            await asyncio.sleep(2.5)

        if True:
            while True:
                print()
                await asyncio.sleep(0.5)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="BLE Gimbal Controller (Hohem Compatible)",
    )
    parser.add_argument("address", type=str, default=None, nargs="?")
    args = parser.parse_args()

    asyncio.run(main(args.address))
