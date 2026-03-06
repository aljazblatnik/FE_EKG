import serial
import serial.tools.list_ports
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

# --- NASTAVITVE ---
BAUD_RATE = 9600

def najdi_com_port():
    """Poskusi samodejno najti ustrezna COM vrata za Arduino."""
    vrata = list(serial.tools.list_ports.comports())
    if not vrata:
        return None
    
    # Če obstajajo samo ena vrata, jih takoj uporabi
    if len(vrata) == 1:
        return vrata[0].device
        
    # Če je priključenih več naprav, poskusi najti Arduino ali klon (CH340 čip)
    for port in vrata:
        if "CH340" in port.description or "Arduino" in port.description or "USB" in port.description:
            return port.device
            
    # Če ne najde nič specifičnega, vzame prva razpoložljiva vrata
    return vrata[0].device

# --- GLOBALNE SPREMENLJIVKE ---
data_buffer = deque([0] * 500, maxlen=500) # Širina grafa (količina shranjenih vzorcev)
beats = deque([0] * 20, maxlen=20)         # Vrsta za povprečenje srčnega utripa (BPM)
beat_old = 0           # Čas zadnjega zabeleženega utripa
current_bpm = 0        # Trenutni srčni utrip
threshold = 620.0      # Prag napetosti za zaznavanje srčnega utripa (R-zobec)
below_threshold = True # Zastavica, ki preprečuje večkratno štetje istega utripa

# --- NASTAVITEV SERIJSKE KOMUNIKACIJE ---
SERIAL_PORT = najdi_com_port()

if SERIAL_PORT is None:
    print("Napaka: Ni mogoče najti nobenih serijskih (COM) vrat. Preveri povezavo z Arduinom!")
    exit()

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Povezava uspešna! Poslušam na vratih {SERIAL_PORT}...")
except Exception as e:
    print(f"Napaka pri odpiranju serijskih vrat {SERIAL_PORT}: {e}")
    exit()

# --- NASTAVITEV GRAFA ---
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=1.5, color='red') # Rdeča barva črte za EKG signal
ax.set_ylim(0, 1024) # Razpon analognega branja (0-1023 na 10-bitnem ADC)
ax.set_xlim(0, 500)  # Širina X osi (prikazuje zadnjih 500 vzorcev)
ax.set_title("EKG Merilnik srčnega utripa")
ax.grid(True, which='both', linestyle='--', linewidth=0.5)

# Oznaka z besedilom za prikaz trenutnega utripa (BPM)
bpm_text = ax.text(0.05, 0.9, 'BPM: 0', transform=ax.transAxes, fontsize=12, 
                   bbox=dict(facecolor='white', alpha=0.8))

def izracunaj_bpm():
    """Izračuna srčni utrip (BPM) na podlagi časa med posameznimi utripi."""
    global beat_old, current_bpm
    current_time = int(time.time() * 1000) # Trenutni čas v milisekundah
    diff = current_time - beat_old
    
    # "Debounce" filter: prezri utripe, ki so si bližje od 250 ms (nemogoč pulz)
    if diff > 250:
        bpm_inst = 60000 / diff # Izračun trenutnega BPM (60.000 ms = 1 minuta)
        beats.append(bpm_inst)
        current_bpm = int(sum(beats) / len(beats)) # Izračun drsečega povprečja
        beat_old = current_time

def posodobi_graf(frame):
    """Funkcija, ki se v zanki kliče za animacijo in posodabljanje grafa."""
    global below_threshold
    
    # Preberi vse podatke, ki čakajo v vmesnem pomnilniku serijskih vrat
    while ser.in_waiting:
        try:
            line_str = ser.readline().decode('utf-8').strip()
            
            # Preveri, ali je prišlo do napake na senzorju (Leads Off) ali drugega besedila
            if line_str == '!' or "Signal" in line_str: 
                # Preskoči cikel, če uporabljamo kodo s tekstovnimi opozorili
                if "Signal" in line_str: continue 
                val = 512.0 # Nastavi sredinsko (ravno) črto, če ni signala
            else:
                val = float(line_str)
                
                # Logika za detekcijo srčnega utripa
                if val > threshold and below_threshold:
                    izracunaj_bpm()
                    below_threshold = False
                elif val < threshold:
                    below_threshold = True

            # Dodaj novo vrednost na konec vrste (stare vrednosti avtomatsko izpadejo)
            data_buffer.append(val)
            
        except ValueError:
            pass # Ignoriraj vrstice, ki niso številke
            
    # Osveži podatke na črti grafa
    line.set_data(range(len(data_buffer)), data_buffer)
    bpm_text.set_text(f'BPM: {current_bpm}')
    return line, bpm_text

# --- ZAGON APLIKACIJE ---
# Zaženi animacijo, ki se osvežuje na 20 milisekund
ani = animation.FuncAnimation(fig, posodobi_graf, interval=20, blit=True)
plt.show()