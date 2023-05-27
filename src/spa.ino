//set trigger to pin 2
int triggerPin =2;

String known_passwordstr = String("sweetdreams");
String input_passwordstr;
char input_password[20];
char tmpChar;
int index;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(triggerPin,OUTPUT);
  tmpChar = "0";
  index = 0;
}

void loop() {
  // wait a litle after starting and clear
  digitalWrite(triggerPin, LOW);
  delay(250);
  Serial.flush();
  Serial.write("Enter password: ");

  // wait for last char
  //while ((tmpChar != '\n') && (index<19)){
  while (tmpChar != '\n'){
    if (Serial.available() >0){
      tmpChar=Serial.read();
      input_password[index++]=tmpChar;
    }
  }

  // null-trminate and strip non-chars
  input_password[index]="\0";
  input_passwordstr = String(input_password);
  input_passwordstr.trim();
  index=0;
  tmpChar=0;

  // set trigger
  digitalWrite(triggerPin,HIGH);

  if(input_passwordstr == known_passwordstr){
    Serial.write("Password is correct!!\n");
  } else {
    //random delay
    delay(random(500));
    Serial.write("Password is NOT correct..\n");
    
  }

}
