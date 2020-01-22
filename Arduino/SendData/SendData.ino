float R1_Pv=34000;
float R2_Pv=10000;
float Ratio_Pv= (R1_Pv + R2_Pv)/R2_Pv;
const int ledPin = 11;
float V_Received = 0;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  // Read the input on analog pin 2 connected to Solar Panel
  // We need a Voltage Divider for Solar Voltage since it takes values between 0-22V. 
  // When R1 = 10V we need R2 = 34000 to decrease the Arduino Voltage to scale from 0-5V. 
   
  float A4_sensorValue = analogRead(A4);
  float V_Out = (A4_sensorValue*5.0)/1023.0;
  float V_Solar = V_Out * Ratio_Pv;
  
  Serial.println(V_Solar);
  
  // Read the input on analog pin 0 connected to Battery. V_max_Battery = 3.7
  float A5_sensorValue = analogRead(A5);
  float V_Battery = (A5_sensorValue *5.0)/1023.0;
  
  Serial.println(V_Battery);

  // Read the input on analog pin 1 connected to Non Invasive Current Sensor  
  float A1_sensorValue = analogRead(A1);
  float i_Battery = map(A1_sensorValue, 0, 1023, -6250, 6250);
  Serial.println(i_Battery);


  // Read the input on analog pin 3 connected to Battery  
  int A0_sensorValue = analogRead(A0);
  float i_Load = map(A0_sensorValue, 0, 1023, -6250,6250);

  Serial.println(i_Load);

  V_Received = Serial.read();
  Serial.println(V_Received);
  
  // Actuation Part: Read the Solar Voltage
  // If V_Received = 18 V-22V, there is excess production. Increase brightness
  // If V_Received = 16-18 V Do nothing 
  // If V_Received = 0-16V Fade the light

  if(V_Received >= 18){
   digitalWrite(ledPin, HIGH);
   Serial.println("LIGHTS ON");
  }

  if(V_Received <= 16){
   digitalWrite(ledPin,map(V_Solar, 0, 22,0,255));
   Serial.println("LIGHTS OFF");
  }
  
  delay(3000);

  ////THERE IS STILL THE LISTEN PART REMAINING: LISTEN BASED ON THE SOLAR VOLTAGE VALUES 
  /// IF A CERTAIN MESSAGE THAN MAKE LED S SHINE

  

}
