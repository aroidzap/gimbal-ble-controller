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
