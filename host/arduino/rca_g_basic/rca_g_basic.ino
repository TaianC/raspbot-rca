// Raspbot Remote Control Application (Raspbot RCA-G), Arduino Instructions for Serial Commandment
// Performs tasks as per requested through serial, also will return sensor when requested.
// Supports Base Part Set.

// 12 and 9 -> MotorDirection and Brake for A
// 13 and 8 -> MotorDirection and Brake for B
// 3 -> Analog motor speed input for A
// 11 -> Analog motor speed input for B
// 10 -> Grove Dust Sensor, input

int incomingData;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  
  pinMode(12, OUTPUT);
  pinMode(9, OUTPUT);

  pinMode(3, OUTPUT);
  pinMode(11, OUTPUT);
  
  pinMode(13, OUTPUT);
  pinMode(8, OUTPUT);
  
  pinMode(10, INPUT);
}

void loop() {
  // key
  // & = Compatability Check
  // F, B, Arrest = Forwards, Backwards, Arrest
  // W, X = Right Forwards, Backwards
  // Y, Z = Left Forwards, Backwards
  // S = Spin Clockwise
  // C = Spin Counterclockwise

  if (Serial.available() > 0) {

    incomingData = Serial.read();
    
    if (incomingData == 'F') {
      digitalWrite(12, HIGH);
      digitalWrite(9, LOW);
      analogWrite(3, 255);
      
      digitalWrite(13, LOW);
      digitalWrite(8, LOW);
      analogWrite(11, 255);
      
      delay(1000);
    }
    
    if (incomingData == 'B') {
      digitalWrite(12, LOW);
      digitalWrite(9, LOW);
      analogWrite(3, 255);
      
      digitalWrite(13, HIGH);
      digitalWrite(8, LOW);
      analogWrite(11, 255);
      
      delay(1000);
    }
    
    if (incomingData == 'A') {
      digitalWrite(9, HIGH);
      analogWrite(3, 0);
      
      digitalWrite(8, HIGH);
      analogWrite(11, 0);  
    }
    
    if (incomingData == 'W') {
      digitalWrite(13, LOW);
      digitalWrite(8, LOW);
      analogWrite(11, 255);
      
      digitalWrite(9, HIGH);
      analogWrite(3, 0);
      
      delay(1000);
    }
    
    if (incomingData == 'X') {
      digitalWrite(13, HIGH);
      digitalWrite(8, LOW);
      analogWrite(11, 255);
      
      digitalWrite(9, HIGH);
      analogWrite(3, 0);
      
      delay(1000);
    }
    
    if (incomingData == 'Y') {
      digitalWrite(8, HIGH);
      analogWrite(11, 0);
      
      digitalWrite(12, HIGH);
      digitalWrite(9, LOW);
      analogWrite(3, 255); 
      
      delay(1000);
    }
    
    if (incomingData == 'Z') {
      digitalWrite(8, HIGH);
      analogWrite(11, 0);
      
      digitalWrite(12, LOW);
      digitalWrite(9, LOW);
      analogWrite(3, 255); 
      
      delay(1000);
    }
    
    if (incomingData == 'S') {
      digitalWrite(13, HIGH);
      digitalWrite(8, LOW);
      analogWrite(3, 255); 
      
      digitalWrite(12, HIGH);
      digitalWrite(9, LOW);
      analogWrite(3, 255);
      
      delay(1000);
    }
    
    if (incomingData == 'C') {
      digitalWrite(13, HIGH);
      digitalWrite(8, LOW);
      analogWrite(3, 255); 
      
      digitalWrite(12, LOW);
      digitalWrite(9, LOW);
      analogWrite(3, 255);
      
      delay(1000);
    }
  }
}
