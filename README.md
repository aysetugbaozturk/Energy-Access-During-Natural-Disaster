# Energy-Access-During-Natural-Disaster
This project consists of the software component that I was responsible for of a Cyber-Physical Solar Pv-Battery-Load Management project. The other parts of the project are Hardware, Data Analysis and Prototyping. The software component mantains the communications between the different components. It stars with gathering data from the Arduino using sensors and ends with updating user via text messages. The project particularly focuses on solving the energy access problem during natural disasters using a simple nanogrid. <br>

Steps: 
1. To start a local server run wallflower_pico_master/wallflower_pico_server.py
2. Once the hardware is ready and sensors are connected, run senddata.ino to initiate data collection. 
3. Run ... to collect data from Arduino and send it to the local server for storage. 
4. Run ListenandProcess to receive data from the server, perform data analysis and communicate results with the user via text message**. 

Note:
*wallflower is a
\**Twillio is used for sending text messages
