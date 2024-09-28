// Define motor control pins
const int ENA = 5; // Enable pin for Motor 2 (A7) red
const int IN1 = 3; // Input 1 pin for Motor 2 (D3) Orange
const int IN2 = 2; // Input 2 pin for Motor 2 (D2) Yellow
const int ENB = 6; // Enable pin for Motor 1 (A0) purple
const int IN3 = 12; // Input 1 pin for Motor 1 (D12) Blue
const int IN4 = 11; // Input 2 pin for Motor 1 (D11) Green

void setup() {
  // Initialize motor control pins as outputs
  Serial.begin(115200);
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    String incomingString = Serial.readStringUntil('\n'); // Read until comma
    incomingString.trim();  // Remove leading/trailing spaces

    if (incomingString.indexOf(',') != -1) {
      // Split the string at the comma
      int commaIndex = incomingString.indexOf(',');
      String speedAString = incomingString.substring(0, commaIndex);
      String speedBString = incomingString.substring(commaIndex + 1);

      // Convert strings to integers and determine direction
      int speedA = speedAString.toInt();
      bool forwardA = speedA >= 0;
      speedA = abs(speedA);  // Use absolute value for speed

      int speedB = speedBString.toInt();
      bool forwardB = speedB >= 0;
      speedB = abs(speedB);  // Use absolute value for speed

      SetMotorA(speedA, forwardA);  // Set Motor A's speed and direction
      SetMotorB(speedB, forwardB);  // Set Motor B's speed and direction
    } else {
      Serial.println(incomingString);
      Serial.println("Invalid input format. Please use <motorA, motorB>");
    }
  }
}

void StopMotors() {
  analogWrite(ENA, 0); // Stop Motor A
  analogWrite(ENB, 0); // Stop Motor B
  delay(1000); // Wait for 1 second
}

void SetMotorA(int speed, bool forward) {
  digitalWrite(IN1, forward ? HIGH : LOW);
  digitalWrite(IN2, forward ? LOW : HIGH);
  analogWrite(ENA, speed);
}

void SetMotorB(int speed, bool forward) {
  digitalWrite(IN3, forward ? HIGH : LOW);
  digitalWrite(IN4, forward ? LOW : HIGH);
  analogWrite(ENB, speed);
}