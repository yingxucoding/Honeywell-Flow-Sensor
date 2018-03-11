#include<Wire.h>
#define sensor 0x49 //Unique bus address 

void setup()
{ 
  Wire.begin();//Wakes up I2C bus 
  Serial.begin(9600);
}

void getdata(byte *a, byte *b)
{
  //Move register pointer back to first register
  //Wire.beginTransmission(sensor);
  //Wire.write(1);
  //Wire.endTransmission();
  Wire.requestFrom(sensor,2);//Sends content of first two registers
  *a = Wire.read(); //first byte recieved stored here
  *b = Wire.read(); //second byte recieved stored here
}

void showdata()
{
  byte aa,bb;
  float flow;  // flow reading in SLPM
  float FS = 50;  // full scale flow  in SLPM from sensor's data sheet
  getdata(&aa,&bb);
  //Serial.print("byte 1: "); Serial.println(aa);
  //Serial.print("byte 2: "); Serial.println(bb);
  flow = FS * ((float(aa) * 256 + float(bb)) / 16384 - 0.1) / 0.8;  // equation from data sheet
  //Serial.print("Flow: "); 
  Serial.println(flow); 
  //Serial.println(" SLPM");
  delay(100);

}

void loop()
{
  showdata();
}

