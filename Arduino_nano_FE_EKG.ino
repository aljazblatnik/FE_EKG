void setup() {
  // Inicializacija serijske komunikacije pri hitrosti 9600 baudov:
  Serial.begin(9600);
  
  // Nastavitev digitalnih pinov za zaznavanje odklopljenih elektrod (Leads Off):
  pinMode(9, INPUT);  // Nastavitev za detekcijo odklopa pozitivne elektrode (LO +)
  pinMode(10, INPUT); // Nastavitev za detekcijo odklopa negativne elektrode (LO -)
}

void loop() {
  // Branje analogne vrednosti iz EKG senzorja (pin A0) in 
  // pošiljanje prebranega vzorca na serijski port:
  Serial.println(analogRead(A0));
  
  // Kratka zakasnitev (1 milisekunda) med posameznimi meritvami,
  // ki preprečuje preobremenitev serijske komunikacije:
  delay(1);
}