//Libraries for LoRa
#include <SPI.h>
#include <LoRa.h>

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

String LoRaData;

void setup() { 
  //initialize Serial Monitor
  Serial.begin(9600);
  Serial.println("LoRa Receiver Test");
  
  //setup LoRa transceiver module
  LoRa.setPins(SS, RST, DIO2);

  if (!LoRa.begin(BAND)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  Serial.println("LoRa Initializing OK!");
  
}

void loop() {

  //try to parse packet
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    //read packet
    while (LoRa.available()) {
      LoRaData = LoRa.readString();
      Serial.print(LoRaData);
      Serial.println();
      delay(1000);
    }
 }

}
