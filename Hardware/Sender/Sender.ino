#include <Wire.h>
//Libraries for LoRa
#include <SPI.h>
#include <LoRa.h>
#include <Adafruit_BMP085.h>
#include <dht.h>  // Include DHT11 library

#define seaLevelPressure_hPa 1013.25
#define DATApin 4  // Defines Arduino pin which is connected to the sensor
//define the pins used by the LoRa transceiver module
#define SCK 13
#define MISO 12
#define MOSI 11
#define SS 10
#define RST 9
#define DIO2 2

//433E6 for Asia
//866E6 for Europe
//915E6 for North America
#define BAND 433E6

dht DHT;      // Creates a DHT object
Adafruit_BMP085 bmp;

void setup() 
 {
  //Sets the baud for serial data transmission between Arduino and your computer
  Serial.begin(9600);
  Serial.println("LoRa Sender Test");
  //setup LoRa transceiver module
  LoRa.setPins(SS, RST, DIO2);
  
  if (!LoRa.begin(BAND)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  Serial.println("LoRa Initializing OK!");
  if (!bmp.begin()) {
  Serial.println("Could not find a valid BMP085 sensor, check wiring!");
  while (1) {}
  }
 }

void loop() 
 {
  // Read data from Sensor
  int readData = DHT.read11(DATApin);

  float TC = DHT.temperature;  // Read Temperature in Degree Celsius unit
  float TF = ((TC*9.0)/5.0+32.0); // Convert Celsius to Fahrenheit unit
  
  float h = DHT.humidity;   // Read humidity

  //Print Tempareture Value on Serial Monitor Window
  Serial.print("Temperature = ");
  Serial.print(TC);  // Temperature value in Degree Celsius
  Serial.println("°C | ");
  Serial.print(TF);  // Temperature value in Fahrenheit
  Serial.println("°F ");

  //Print Humidity Value on Serial Monitor Window
  Serial.print("Humidity = ");
  Serial.print(h);
  Serial.println("% ");

  Serial.print("Temperature = ");
  Serial.print(bmp.readTemperature());
  Serial.println(" *C");
 
  Serial.print("Pressure = ");
  Serial.print(bmp.readPressure());
  Serial.println(" Pa");

  Serial.print("Altitude = ");
  Serial.print(bmp.readAltitude());
  Serial.println(" meters");
  
  Serial.print("Pressure at sealevel (calculated) = ");
  Serial.print(bmp.readSealevelPressure());
  Serial.println(" Pa");

  Serial.print("Real altitude = ");
  Serial.print(bmp.readAltitude(seaLevelPressure_hPa * 1000));
  Serial.println(" meters");
    
  Serial.println();

   //Send LoRa packet to receiver
  LoRa.beginPacket();
  LoRa.print(TC);
  LoRa.print(',');
  LoRa.print(TF);
  LoRa.print(',');
  LoRa.print(h);
  LoRa.print(',');
  LoRa.print(bmp.readTemperature());
  LoRa.print(',');
  LoRa.print(bmp.readSealevelPressure());
  LoRa.print(',');
  LoRa.print(bmp.readAltitude(seaLevelPressure_hPa * 1000));
  LoRa.endPacket();

  delay(2000); // wait two seconds
}
