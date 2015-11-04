import math


# Inputs
FuelFlow = 1500                         # Fuel Flow from aircraft manual or cockpit instrumentation (kg/s or lbm/hr)
AmbientPressure = 14.696                # Inlet Ambient Pressure (psia)
AmbientTemperature = 15                 # Inlet Ambient Temperature (degrees celsius)
Mach = 1                                # Mach Number
RelativeHumidity = .6                   # Relative Humidity 60%

def bffm2(FuelFlow, AmbientPressure, AmbientTemperature, Mach, RelativeHumidity):
    # Define some more things
    AmbientPressureFactor = AmbientPressure /14.696 # Ratio of inlet over sea level pressure
    AmbientTemperatureFactor = (AmbientTemperature/ + 273.15)/288.15 # Ratio of inlet over sea level temperature
    beta = 7.90298*(1- 373.16/(AmbientTemperature+273.16) + 3.00571 + 5.02808*math.log10(373.1))
    SatVaporPressure = 0.014504*10**beta # Saturation Vapor Pressure (psia)
    SpecificHumidity = 0.62198*RelativeHumidity*SatVaporPressure/(AmbientPressure - RelativeHumidity*SatVaporPressure) # Specific humidity (lbm H2O / lbm air)

    # Data from graph fit - Reference Emission Index corrected for installation effects (lbm species/1000lbm of fuel)
    REICO, REIHC, REINOx = graphfit()

    # Fuel Flow Correction - Includes installation effects cause by engine air bleed (kg/s or lbm/hr)
    FuelFlowCorrected = FuelFlow / AmbientPressureFactor * AmbientTemperatureFactor**3.8 * math.exp(0.2*Mach**2)

    # Carbon Monoxide Correction = Emissions Index of CO
    EICO = REICO * (AmbientTemperatureFactor**3.8 / AmbientPressureFactor**1.02)

    # Hydrocarbon Correction = Emissions Index of HC
    EIHC = REIHC * (AmbientTemperatureFactor**3.8 / AmbientPressureFactor**1.02)

    # Nitrogen Oxide Correction = Emissions Index of NOx
    EINOx = REINOx * math.exp(-19 * (SpecificHumidity - 0.0063)) * math.sqrt(AmbientPressureFactor**1.02/AmbientTemperatureFactor**3.3)
    return [FuelFlowCorrected,EICO,EIHC,EINOx]

def graphfit():
    REICO = 1
    REIHC = 1
    REINOx = 1
    return REICO, REIHC, REINOx

print(bffm2(FuelFlow,AmbientPressure,AmbientTemperature,Mach,RelativeHumidity))