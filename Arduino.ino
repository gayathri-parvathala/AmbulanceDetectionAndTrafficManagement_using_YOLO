const int greenLight1 = 4; 
const int redLight1 = 2;    
const int greenLight2 = 7;  
const int redLight2 = 5;    
const int greenLight3 = 10; 
const int redLight3 = 8;    
const int greenLight4 = 13; 
const int redLight4 = 11;   

bool isActive = false;         
unsigned long lastActivatedTime = 0; 
int currentModule = 0;         
unsigned long cycleStartTime = 0; 
char lastCommand = '0';       
void setup() {
  pinMode(greenLight1, OUTPUT);
  pinMode(redLight1, OUTPUT);
  pinMode(greenLight2, OUTPUT);
  pinMode(redLight2, OUTPUT);
  pinMode(greenLight3, OUTPUT);
  pinMode(redLight3, OUTPUT);
  pinMode(greenLight4, OUTPUT);
  pinMode(redLight4, OUTPUT);

  Serial.begin(9600); 
  cycleStartTime = millis(); 
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read(); 
    Serial.print("Received command: "); /
    Serial.println(command); 
    if (!isActive && command != lastCommand) {
      isActive = true; 
      lastCommand = command; 
      deactivateAllLights();
      if (command == '1') {
        activateTrafficModule(greenLight1, redLight1); 
        currentModule = 0; 
      } else if (command == '2') {
        activateTrafficModule(greenLight2, redLight2); 
        currentModule = 1; 
      } else if (command == '3') {
        activateTrafficModule(greenLight3, redLight3); 
        currentModule = 2; 
      } else if (command == '4') {
        activateTrafficModule(greenLight4, redLight4); 
        currentModule = 3; /
      }

      lastActivatedTime = millis(); 
    }
  } 
  if (isActive && (millis() - lastActivatedTime >= 10000)) {
    deactivateAllLights(); 
    isActive = false; 
    cycleStartTime = millis(); 
  }
  if (!isActive) {
    if (millis() - cycleStartTime >= 5000) {
      deactivateAllLights(); 
      // Activate the green light for the current road
      if (currentModule == 0) {
        digitalWrite(greenLight1, HIGH); 
        digitalWrite(redLight1, LOW);     
        currentModule = 1; 
      } else if (currentModule == 1) {
        digitalWrite(greenLight2, HIGH); 
        digitalWrite(redLight2, LOW);     
        currentModule = 2; 
      } else if (currentModule == 2) {
        digitalWrite(greenLight3, HIGH); 
        digitalWrite(redLight3, LOW);     
        currentModule = 3; // Move to next module
      } else if (currentModule == 3) {
        digitalWrite(greenLight4, HIGH); 
        digitalWrite(redLight4, LOW);     
        currentModule = 0; 
      }

      cycleStartTime = millis(); 
    }
  }
}

void activateTrafficModule(int greenPin, int redPin) {
  digitalWrite(greenPin, HIGH); 
  digitalWrite(redPin, LOW);    
}

void deactivateAllLights() {
  digitalWrite(greenLight1, LOW);
  digitalWrite(redLight1, HIGH);
  digitalWrite(greenLight2, LOW);
  digitalWrite(redLight2, HIGH);
  digitalWrite(greenLight3, LOW);
  digitalWrite(redLight3, HIGH);
  digitalWrite(greenLight4, LOW);
  digitalWrite(redLight4, HIGH);
}
