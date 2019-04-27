# PID_motor
# PID_v1 é o sketch do arduino que estou utilizando.

 Tentei adcionar controle anti windup, creio estar correto.
 
 Não consegui me livrar do cap na resposta, se esta não for limitada o sistema se torna incrivelmente instável.
 
 Estou medindo o tempo de execução dt. O problema é que ele é muito pequeno, e muitas vezes o retorno é 0, então coloquei o limite inferior de 1 milisegundo.


 Os valores das contantes podem ser inseridos sem reiniciar a placa, pq sou preguiçoso (a porta usb do meu computador fica longe).
 é só digitar: s kp ki kd. Nem sempre o controlador pega o input, mas funciona bem para testar o código.
