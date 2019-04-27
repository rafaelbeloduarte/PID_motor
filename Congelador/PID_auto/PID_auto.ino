#include <PID_v1.h>

#define LED_pin 9
#define LDR_pin A0
#define setpoint_pin A5


double input;
double setpoint;
double output;
double outputMin; 
double outputMax; 
double Kp;
double Ki; 
double Kd;
double incremento, decremento;
int i;
double e, derivada, t, soma_erro;
const int sampleRate = 1;        // O intervalo do controle PID

PID myPID(&input, &output, &setpoint, Kp, Ki, Kd, DIRECT);

void setup() {
  Serial.begin(115200);
  myPID.SetMode(AUTOMATIC);                          // Ligar o controle PID
  myPID.SetSampleTime(sampleRate); 
 /* pinMode(3, INPUT);
  pinMode(2, INPUT);
  pinMode(4, INPUT);*/
  pinMode(LED_pin, OUTPUT);
  pinMode(LDR_pin, INPUT);
  pinMode(setpoint_pin, INPUT);
  e = 0;
  derivada = 0;
  soma_erro = 0;
  t = 100;
  Kp = 0.924;
  Ki = 9.24; 
  Kd = 0.0231;
  setpoint = 220;
  outputMin = 0;
  outputMax = 246;
  incremento = 0.05; 
  decremento = 0.05;
  i = 1;
}

void loop() {
 // AutoPID myPID(&input, &setpoint, &output, outputMin, outputMax, Kp, Ki, Kd); //library AutoPID.h
  //input => ler LDR
  //output => intensidade da luz

  setpoint = map(analogRead(setpoint_pin), 0, 1023, 0, 255);
  Serial.print("setpoint = ");
  Serial.print(setpoint);
  Serial.print("\t");

  input = map(analogRead(LDR_pin), 0, 1023, 0, 255);
  analogWrite(LED_pin, output);
  myPID.Compute();  
/*  Serial.print("output = ");
  Serial.print(output);
  Serial.print("\t");*/
  Serial.print("input = ");
  Serial.print(input);
  Serial.print("\t");

  Serial.print("output = ");
  Serial.println(output);
//  myPID.run();
  if (Serial.available() > 0)
 {
 for (int x = 0; x < 4; x++)
 {
 switch(x)
 {
 case 0:
 Kp = Serial.parseFloat();
 break;
 case 1:
 Ki = Serial.parseFloat();
 break;
 case 2:
 Kd = Serial.parseFloat();
 break;
 case 3:
 for (int y = Serial.available(); y == 0; y--)
 {
 Serial.read();
 }
 break;
 }
 }
 Serial.print(" Kp,Ki,Kd = ");  // Display the new parameters
 Serial.print(Kp);
 Serial.print(",");
 Serial.print(Ki);
 Serial.print(",");
 Serial.println(Kd);
 myPID.SetTunings(Kp, Ki, Kd);  // Set the tuning of the PID loop
 }
  
  
 /* derivada = (e - (setpoint - input)) / (t / 1000);
  soma_erro += e * (t / 1000);
  e = setpoint - input;

    Serial.print("derivada = ");
  Serial.print(derivada);
  Serial.print("\t");

  Serial.print("soma_erro = ");
  Serial.print(soma_erro);
  Serial.print("\t");

  Serial.print("erro = ");
  Serial.print(e);
  Serial.print("\t");*/
  
/*  //kp incremento
    if (abs(e) >= 1) {
      Kp = Kp + incremento;
    }
    else {
      if (Kp > 0) {
        Kp = Kp - decremento;
      }
      else{
        Kp = 0;
      }
     }
  //ki incremento
    if (abs(e) > 10) {
      Ki = Ki + incremento;
    }
    else {
      if (Ki > 0) {
        Ki = Ki - decremento;
      }
      else{
        Ki = 0;
      }
    }
  //kd incremento
    if (abs(derivada) > 10) {
      Kd = Kd + incremento;
    }
    else {
      if (Kd > 0) {
        Kd = Kd - decremento;
      }
      else{
        Kd = 0;
      }
    }*/

  /*//para trocar os botões + - entre as constantes
  if(digitalRead(4) == HIGH){
    i = i + 1;
    if(i == 4){
      i = 1;
      }
    Serial.print(i*30);
    Serial.print("\t");
    }
  
  // uso botões para ajustar manualmente as constantes
  //kp incremento
  if(i == 1){
    if (digitalRead(2) == HIGH) {
      Kp = Kp + incremento;
    }
    if(digitalRead(3) == HIGH) {
      if (Kp > 0) {
        Kp = Kp - decremento;
      }
    else{
      Kp = 0;
      }
    }
   }
  //ki incremento
  if(i == 2){
    if (digitalRead(2) == HIGH) {
      Ki = Ki + incremento;
    }
    if(digitalRead(3) == HIGH) {
      if (Ki > 0) {
        Ki = Ki - decremento;
      }
      else{
        Ki = 0;
      }
    }
  }
  //kd incremento
  if(i == 3){
    if (digitalRead(2) == HIGH) {
      Kd = Kd + incremento;
    }
    if(digitalRead(3) == HIGH) {
      if (Kd > 0) {
        Kd = Kd - decremento;
      }
      else{
        Kd = 0;
      }
    }
  }*/

 /* Serial.print("Kp = ");
  Serial.print(Kp*10);
  Serial.print("\t");

  Serial.print("Ki = ");
  Serial.print(Ki*10);
  Serial.print("\t");

  Serial.print("Kd = ");
  Serial.println(Kd*10);*/
  delay(t);
}
