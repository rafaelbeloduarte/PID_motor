#define pino_LED 9
#define pino_LDR A0
#define pino_pot A5

/*equação:  Resposta = P*erro + I*(soma(0,t)erro*delta t) + D*(erro_ant - erro_atual)/delta t */
float r;
float t = 100;
float LDR_valor, e, kp = 1.35, ki = .25, kd = .0,  soma_erro, derivada, set_point, dt, tempo_atual;
long timer, timer2;
char ler = 'n';
int contador = 0;
float incremento = 0.05, decremento = 0.05;

void setup() {
  Serial.begin(115200);
  pinMode(pino_LED, OUTPUT);

  Serial.println("Inserir valores(kp, ki, kd)");
  while (Serial.available() == 0);
  kp = Serial.parseFloat();
  Serial.print("kp ");
  Serial.println(kp);
  while (Serial.available() == 0);
  ki  = Serial.parseFloat();
  Serial.print("ki ");
  Serial.println(ki);
  while (Serial.available() == 0);
  kd  = Serial.parseFloat();
  Serial.print("kd ");
  Serial.println(kd);
}

void loop() {
  tempo_atual = millis();

  if (r > 255) {
    r = 255;
  }
  if (r <= 0) {
    r = 0;
  }

  LDR_valor = map(analogRead(pino_LDR), 0, 1023, 0, 255);
  analogWrite(pino_LED, r);

  if (millis() > 300 + timer) {

    set_point = map(analogRead(pino_pot), 0, 1023, 0, 255);
    Serial.print("set_point = ");
    Serial.print(set_point);
    Serial.print("\t");

    Serial.print("soma_erro = ");
    Serial.print(soma_erro);
    Serial.print("\t");

    Serial.print("LDR = ");
    Serial.print(LDR_valor);
    Serial.print("\t");

    Serial.print("r = ");
    Serial.print(r);
    Serial.print("\t");

    Serial.print("kp = ");
    Serial.print(kp);
    Serial.print("\t");

    Serial.print("ki = ");
    Serial.print(ki);
    Serial.print("\t");

    Serial.print("kd = ");
    Serial.println(kd);
    timer = millis();
  }

  dt = millis() - tempo_atual;

  if (dt < 1) {
    dt = 1;
  }

  derivada = ((set_point - LDR_valor) - e) / (dt);

  e = set_point - LDR_valor;

  soma_erro += e * dt;

  r = kp * e + ki * soma_erro + kd * derivada;

}
