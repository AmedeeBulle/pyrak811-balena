Basic RAK811 example with balenaCloud
=====================================

This is a basic example on how to use [PiSupply IoT LoRa Node pHAT for Raspberry Pi ](https://uk.pi-supply.com/products/iot-lora-node-phat-for-raspberry-pi) with [balenaCloud](https://www.balena.io/).

The application will join [TheThingsNetwork](https://www.thethingsnetwork.org) using OTAA and send the CPU temperature in [Cayenne LPP](https://mydevices.com/cayenne/docs/lora/#lora-cayenne-low-power-payload) format every 5 minutes.

All you need to do is:
- Create an application in [balenaCloud](https://www.balena.io/), add a device, flash the generated image on an SD Card and boot your Raspberry Pi with it
- When your device appears in the [balenaCloud](https://www.balena.io/) console, go to `Device Configuration` and ensure that `UART` is enabled
- Clone this repository
- Add the balena repo with  
`git remote add balena YourAccount@git.balena-cloud.com:YourAccount/YourApplication.git`  
(copy this line from your [balenaCloud](https://www.balena.io/) console)
- Push the application to [balenaCloud](https://www.balena.io/) with:  
`git push balena master`  
The code will be pushed to your device after a few minutes. Note the `Device EUI` which will be printed in the `Logs` window.
- Create an application in [TheThingsNetwork](https://www.thethingsnetwork.org) and register your device.  
Enter the `Device EUI` copied from previous step
- Back to the [balenaCloud](https://www.balena.io/) console, create 2 Service variables:
  - `APP_EUI` with `App EUI` copied from [TheThingsNetwork](https://www.thethingsnetwork.org) console
  - `APP_KEY` with `App Key` copied from [TheThingsNetwork](https://www.thethingsnetwork.org) console

Your application will restart and send the CPU temperature to [TheThingsNetwork](https://www.thethingsnetwork.org) every 5 minutes.

# Optional Service variables
- `SERIAL_PORT`: The default serial port is `/dev/ttyS0`, depending on your Raspberry Pi model and configuration you might have to override the default (e.g. `/dev/ttyAMA0`)
- `BAND`: The default LoRaWan region is `EU868`, you can set this variable to match your region (supported regions are: `EU868`, `US915`, `AU915`, `KR920`, `AS923`, `IN865`)
