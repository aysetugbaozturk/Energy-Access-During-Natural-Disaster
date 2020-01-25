# Energy-Access-During-Natural-Disaster
This project consists of the software component that I was responsible for of a Cyber-Physical Solar Pv-Battery-Load Management project. The other parts of the project are Hardware, Data Analysis and Prototyping. The software component mantains the communications between the different components. It stars with gathering data from the Arduino using sensors and ends with updating user via text messages. The project particularly focuses on solving the energy access problem during natural disasters using a simple nanogrid. Arduino, Python, JavaScript and html programming languages are used in this project. <br>

Schematic representation: 
![alt text](https://github.com/aysetugbaozturk/Energy-Access-During-Natural-Disaster/blob/master/Connectivity_186.jpg)




Steps: 
1. To start a local server run wallflower_pico_master/wallflower_pico_server.py*
2. Once the hardware is ready and sensors are connected, run Arduino/SendData/SendData.ino to initiate data collection. 
3. Run ListenandSend.py to collect data from Arduino and send it to the local server for storage. 
4. Run ListenandProcess.py to receive data from the server, perform data analysis and communicate results with the user via text message**. 

Note: <br>
*Wallflower.Pico (https://github.com/wallflowercc/wallflower-pico), is a Internet of Things platform with a RESTful Web API for storing and retrieving time series data (int, float, or string).<br>
\**Twillio(https://www.twilio.com/sms) is used for sending text messages
