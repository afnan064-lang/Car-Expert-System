"""Knowledge base: 100 IF-THEN rules over 300 assertions (200 symptoms + 100 diagnoses).

Rule format: (id, category, [conditions], diagnosis, severity, advice)
A condition starting with "@" refers to another diagnosis (rule chaining).
"""
from collections import namedtuple

Rule = namedtuple("Rule", "id category conditions conclusion severity advice")

_RAW = [
    # ---------------- 1. Starting & Battery ----------------
    ("Starting & Battery", ["Engine does not crank", "Dashboard lights are dim or off"], "Dead or discharged battery", "Medium", "Jump-start the car, then test and charge or replace the battery."),
    ("Starting & Battery", ["Clicking sound when turning key", "White or green powder on battery terminals", "Car starts only after several attempts"], "Corroded battery terminals", "Low", "Clean terminals with baking soda and water; tighten the clamps."),
    ("Starting & Battery", ["Engine does not crank", "Single loud click when turning key", "Dashboard lights are bright"], "Faulty starter motor", "High", "Have the starter motor tested and replaced if needed."),
    ("Starting & Battery", ["Battery warning light is on", "Headlights dim while driving", "Engine stalls while driving"], "Failing alternator", "High", "Test the alternator output; replace it if below 13.5 V."),
    ("Starting & Battery", ["Squealing noise from engine bay", "Battery warning light is on"], "Loose or worn serpentine belt", "Medium", "Inspect and tension or replace the drive belt."),
    ("Starting & Battery", ["Key turns but nothing happens", "Dashboard lights flicker when key is turned", "Key is hard to turn"], "Faulty ignition switch", "Medium", "Replace the ignition switch; check the key for wear."),
    ("Starting & Battery", ["Security or key light is flashing", "Engine cranks but does not start"], "Immobilizer or key fob fault", "Medium", "Try the spare key; reprogram the key at a dealer or locksmith."),
    ("Starting & Battery", ["Nothing happens when turning key", "Dashboard lights are bright", "No click sound"], "Faulty starter relay or fuse", "Low", "Check and replace the starter relay and fuse."),
    ("Starting & Battery", ["Battery drains overnight", "Interior light stays on after locking"], "Parasitic battery drain", "Medium", "Find the circuit drawing current with a multimeter and repair it."),
    ("Starting & Battery", ["@Dead or discharged battery", "Battery is more than four years old"], "Battery replacement required", "Medium", "Replace the battery with one of the correct rating."),

    # ---------------- 2. Engine Performance ----------------
    ("Engine Performance", ["Engine shakes at idle", "Check engine light is flashing", "Jerking during acceleration"], "Spark plug or ignition coil failure", "High", "Replace spark plugs and test ignition coils; avoid hard driving."),
    ("Engine Performance", ["Reduced engine power", "Black smoke from exhaust", "Air filter looks very dirty"], "Clogged air filter", "Low", "Replace the air filter."),
    ("Engine Performance", ["Rough idle", "Hissing sound from engine bay"], "Vacuum leak", "Medium", "Inspect vacuum hoses and intake gaskets; replace cracked parts."),
    ("Engine Performance", ["Engine hesitates when accelerating", "Poor fuel economy", "Engine stalls after starting"], "Dirty or faulty mass airflow sensor", "Medium", "Clean the MAF sensor with MAF cleaner or replace it."),
    ("Engine Performance", ["Ticking or slapping noise from engine front", "Engine cranks but does not start", "Timing belt is past service interval"], "Timing belt failure", "Critical", "Stop driving. Have the timing belt and engine inspected immediately."),
    ("Engine Performance", ["Oil pressure warning light is on", "Engine knocking noise"], "Low oil pressure", "Critical", "Switch off the engine now; check the oil level and tow if needed."),
    ("Engine Performance", ["Oil spots under the car", "Burning oil smell", "Oil level drops between changes"], "Engine oil leak", "Medium", "Find the leak (valve cover, oil pan, seals) and repair it."),
    ("Engine Performance", ["White smoke from exhaust", "Coolant level keeps dropping", "Milky oil on dipstick"], "Blown head gasket", "Critical", "Stop driving; engine needs a head gasket repair."),
    ("Engine Performance", ["Blue smoke from exhaust", "Frequent oil top-ups needed"], "Worn piston rings or valve seals", "High", "Do a compression test; plan an engine overhaul."),
    ("Engine Performance", ["Engine idles too high or too low", "Accelerator pedal feels unresponsive"], "Dirty throttle body", "Low", "Clean the throttle body; perform an idle relearn."),

    # ---------------- 3. Fuel System ----------------
    ("Fuel System", ["Fuel gauge reads empty", "Engine sputters and stops"], "Out of fuel", "Low", "Add fuel; if it still fails, check the fuel gauge sender."),
    ("Fuel System", ["Whining noise from fuel tank", "Engine loses power under load"], "Failing fuel pump", "High", "Test fuel pressure; replace the fuel pump."),
    ("Fuel System", ["Engine hesitates when accelerating", "Hard starting", "Fuel filter has not been changed for a long time"], "Clogged fuel filter", "Medium", "Replace the fuel filter."),
    ("Fuel System", ["Rough idle", "Fuel smell from exhaust", "Poor fuel economy"], "Dirty or leaking fuel injectors", "Medium", "Use an injector cleaner or have the injectors cleaned or replaced."),
    ("Fuel System", ["Engine problems began after refueling", "Engine knocking noise"], "Contaminated or low-octane fuel", "Medium", "Drain the tank if contaminated; refill with correct-grade fuel."),
    ("Fuel System", ["Strong petrol smell near car", "Wet fuel spots under the car"], "Fuel line or tank leak", "Critical", "Do not start the engine. Tow the car; fire hazard."),
    ("Fuel System", ["Check engine light is on", "Fuel cap is loose or missing"], "Faulty fuel cap (EVAP leak)", "Low", "Tighten or replace the fuel cap and clear the code."),
    ("Fuel System", ["Black smoke from exhaust", "Petrol smell in engine oil"], "Faulty fuel pressure regulator", "High", "Replace the regulator and change the engine oil."),
    ("Fuel System", ["Engine misfires after heavy rain or washing", "Fuel was bought at a questionable station"], "Water in fuel", "High", "Drain the tank and fuel lines; replace the fuel filter."),
    ("Fuel System", ["Diesel engine is hard to start in cold", "White smoke at cold start"], "Faulty glow plugs (diesel)", "Medium", "Test and replace the glow plugs."),

    # ---------------- 4. Cooling System ----------------
    ("Cooling System", ["Temperature gauge is in the red zone", "Coolant level is low"], "Low coolant", "High", "Let the engine cool, top up coolant, and look for leaks."),
    ("Cooling System", ["Temperature gauge is in the red zone", "Upper radiator hose is hot but lower hose is cold"], "Thermostat stuck closed", "High", "Replace the thermostat."),
    ("Cooling System", ["Engine takes a long time to warm up", "Cabin heater blows cold air"], "Thermostat stuck open", "Low", "Replace the thermostat."),
    ("Cooling System", ["Coolant leaking near front of engine", "Grinding or whining noise from belt area"], "Failing water pump", "High", "Replace the water pump (and timing belt if driven by it)."),
    ("Cooling System", ["Green or orange puddle under car", "Coolant level is low"], "Radiator or hose leak", "High", "Pressure-test the cooling system; replace the leaking part."),
    ("Cooling System", ["Engine overheats in traffic", "Cooling fan does not spin"], "Faulty radiator fan or relay", "High", "Test the fan motor, relay and fuse; replace the faulty part."),
    ("Cooling System", ["Coolant bubbling in reservoir", "Radiator hose is swollen", "Coolant is pushed out of the reservoir"], "Faulty radiator cap", "Medium", "Replace the radiator cap and inspect hoses."),
    ("Cooling System", ["Engine overheats at highway speed", "Radiator fins are blocked or dirty"], "Clogged radiator", "Medium", "Flush or clean the radiator; replace if internally blocked."),
    ("Cooling System", ["Sweet smell inside cabin", "Windshield fogs with a greasy film"], "Leaking heater core", "Medium", "Replace the heater core."),
    ("Cooling System", ["Temperature gauge fluctuates wildly", "Gauge reads cold despite a warm engine"], "Faulty coolant temperature sensor", "Low", "Replace the coolant temperature sensor."),

    # ---------------- 5. Exhaust & Emissions ----------------
    ("Exhaust & Emissions", ["Rotten egg smell from exhaust", "Reduced engine power", "Check engine light is on"], "Clogged catalytic converter", "High", "Test back-pressure; replace the catalytic converter."),
    ("Exhaust & Emissions", ["Loud rumbling exhaust noise", "Visible rust holes in exhaust"], "Exhaust leak or damaged muffler", "Medium", "Weld or replace the exhaust section."),
    ("Exhaust & Emissions", ["Check engine light is on", "Poor fuel economy", "Failed emissions test"], "Faulty oxygen sensor", "Medium", "Replace the oxygen sensor."),
    ("Exhaust & Emissions", ["Engine pings under acceleration", "Failed emissions test"], "Stuck EGR valve", "Medium", "Clean or replace the EGR valve."),
    ("Exhaust & Emissions", ["Black smoke from exhaust", "Fuel smell from exhaust"], "Engine running too rich", "Medium", "Check sensors, injectors and air filter; scan for codes."),
    ("Exhaust & Emissions", ["Ticking noise that fades when warm", "Exhaust smell inside cabin"], "Cracked exhaust manifold", "High", "Replace the manifold or gasket; exhaust fumes are dangerous."),
    ("Exhaust & Emissions", ["DPF warning light is on", "Diesel engine loses power"], "Clogged diesel particulate filter", "High", "Drive at highway speed to regenerate, or have the DPF cleaned."),
    ("Exhaust & Emissions", ["Rattling noise from under the car", "Rattle when starting engine"], "Broken catalytic converter internals", "Medium", "Replace the catalytic converter."),
    ("Exhaust & Emissions", ["Fuel smell around parked car", "Scan tool shows EVAP code"], "EVAP system leak", "Low", "Smoke-test the EVAP system; replace cracked hoses or valves."),
    ("Exhaust & Emissions", ["Whistling noise from engine under boost", "Loss of power at high RPM", "Blue or grey smoke under acceleration"], "Failing turbocharger", "High", "Inspect the turbo for shaft play and oil leaks; rebuild or replace."),

    # ---------------- 6. Brakes ----------------
    ("Brakes", ["Squealing noise when braking", "Brake warning light is on", "Brake pads look thin on inspection"], "Worn brake pads", "Medium", "Replace the brake pads soon."),
    ("Brakes", ["Grinding noise when braking", "Reduced braking performance"], "Brake pads worn to metal", "Critical", "Stop driving; replace pads and probably the rotors."),
    ("Brakes", ["Steering wheel shakes when braking", "Brake pedal pulsates"], "Warped brake rotors", "Medium", "Resurface or replace the rotors."),
    ("Brakes", ["Brake pedal feels spongy", "Brake fluid level is low"], "Low brake fluid or leak", "Critical", "Do not drive. Check lines, calipers and master cylinder for leaks."),
    ("Brakes", ["Brake pedal sinks slowly to the floor", "No visible brake fluid leak"], "Master cylinder failure or air in brake lines", "Critical", "Bleed the brakes; replace the master cylinder if it persists."),
    ("Brakes", ["Car pulls to one side when braking", "Burning smell after driving", "One wheel is very hot"], "Seized brake caliper", "High", "Replace or rebuild the caliper and the pads on that axle."),
    ("Brakes", ["ABS warning light is on", "Brakes work normally"], "Faulty ABS wheel speed sensor", "Medium", "Scan for ABS codes; clean or replace the wheel speed sensor."),
    ("Brakes", ["Parking brake does not hold", "Parking brake lever has excessive travel"], "Parking brake needs adjustment", "Low", "Adjust the parking brake cable; replace if stretched."),
    ("Brakes", ["Brake pedal is hard to press", "Hissing sound when pressing the brake"], "Failed brake booster", "High", "Test and replace the brake booster or vacuum hose."),
    ("Brakes", ["Scraping noise from rear wheels when braking", "Rear brakes feel weak"], "Worn rear brake shoes or drums", "High", "Replace rear shoes and inspect the drums."),

    # ---------------- 7. Transmission & Drivetrain ----------------
    ("Transmission & Drivetrain", ["Engine revs rise but car does not accelerate", "Burning smell from clutch"], "Worn clutch", "Medium", "Replace the clutch kit and inspect the flywheel."),
    ("Transmission & Drivetrain", ["Gear lever is hard to shift", "Clutch pedal feels stiff or sticks"], "Hydraulic clutch fault", "Medium", "Bleed the clutch hydraulics; replace the clutch master or slave cylinder."),
    ("Transmission & Drivetrain", ["Grinding when changing gears", "Car jumps out of gear"], "Worn synchronizers or gearbox", "High", "Gearbox inspection or rebuild is needed."),
    ("Transmission & Drivetrain", ["Delayed gear engagement", "Red fluid under the car"], "Low automatic transmission fluid", "High", "Fix the leak and refill with the correct ATF."),
    ("Transmission & Drivetrain", ["Automatic transmission slips between gears", "Transmission fluid smells burnt"], "Worn automatic transmission clutches", "High", "Change the fluid and filter; a rebuild may be needed."),
    ("Transmission & Drivetrain", ["Harsh or jerky gear shifts", "Transmission warning light is on"], "Transmission solenoid or control fault", "Medium", "Scan transmission codes; replace the faulty solenoid."),
    ("Transmission & Drivetrain", ["Clicking noise when turning sharply", "Grease on inner wheel or tire"], "Worn CV joint", "Medium", "Replace the CV axle or boot and joint."),
    ("Transmission & Drivetrain", ["Vibration at highway speed", "Clunk when shifting from drive to reverse"], "Worn driveshaft or U-joint", "Medium", "Replace worn U-joints; balance the driveshaft."),
    ("Transmission & Drivetrain", ["Humming noise that rises with speed", "Noise changes when steering left or right"], "Worn wheel bearing", "High", "Replace the wheel bearing."),
    ("Transmission & Drivetrain", ["Whining noise from rear axle", "Gear oil leaking at differential"], "Differential fault", "High", "Refill the gear oil; inspect or rebuild the differential."),

    # ---------------- 8. Steering & Suspension ----------------
    ("Steering & Suspension", ["Steering feels heavy", "Whining noise when turning the wheel"], "Low power steering fluid or failing pump", "Medium", "Top up the fluid, check for leaks, replace the pump if noisy."),
    ("Steering & Suspension", ["Car pulls to one side while driving", "Steering wheel is off-center", "Car drifts when hands are off the wheel"], "Wheel misalignment", "Low", "Get a four-wheel alignment."),
    ("Steering & Suspension", ["Excessive bouncing after bumps", "Nose dives when braking"], "Worn shock absorbers", "Medium", "Replace shocks or struts in pairs."),
    ("Steering & Suspension", ["Clunking noise over bumps", "Loose or wandering steering"], "Worn ball joints or tie rods", "High", "Replace worn joints and then align the wheels."),
    ("Steering & Suspension", ["Rattling over small bumps", "Body roll in corners"], "Worn sway bar links", "Low", "Replace the sway bar links or bushings."),
    ("Steering & Suspension", ["Car sits lower on one corner", "Loud bang when hitting a bump"], "Broken coil spring", "High", "Replace the spring in pairs."),
    ("Steering & Suspension", ["Steering play at center", "Fluid leaking near steering rack"], "Worn or leaking steering rack", "High", "Repair or replace the steering rack."),
    ("Steering & Suspension", ["Creaking noise over speed bumps", "Vague handling"], "Worn suspension bushings", "Low", "Replace worn control arm and sway bar bushings."),
    ("Steering & Suspension", ["Power steering warning light is on", "Steering suddenly becomes heavy"], "Electric power steering fault", "High", "Scan for EPS codes; check battery voltage and the steering motor."),
    ("Steering & Suspension", ["Knocking noise from front when turning", "Steering wheel does not return to center"], "Worn strut mounts or bearings", "Medium", "Replace the strut mount and bearing."),

    # ---------------- 9. Tires & Wheels ----------------
    ("Tires & Wheels", ["Tire pressure warning light is on", "Tire looks flat", "Ride feels soft and sluggish"], "Low tire pressure", "Medium", "Inflate to the recommended pressure and check for leaks."),
    ("Tires & Wheels", ["Tire loses air repeatedly", "Nail or object stuck in tire"], "Punctured tire", "Medium", "Repair or replace the tire at a tire shop."),
    ("Tires & Wheels", ["Steering wheel vibrates at 80-100 km/h", "Uneven tread wear"], "Unbalanced wheels", "Low", "Balance the wheels."),
    ("Tires & Wheels", ["Inner tire edge is worn", "Car pulls to one side while driving"], "Incorrect toe or camber alignment", "Medium", "Get an alignment and check suspension parts."),
    ("Tires & Wheels", ["Tire center tread is worn", "Tire pressure is above recommendation"], "Over-inflated tires", "Low", "Reduce pressure to the placard value."),
    ("Tires & Wheels", ["Both tire edges are worn", "Tire pressure is below recommendation"], "Under-inflated tires", "Low", "Inflate to the placard value; check monthly."),
    ("Tires & Wheels", ["Scalloped or cupped tire wear", "Excessive bouncing after bumps"], "Worn suspension causing tire cupping", "Medium", "Replace worn shocks and rotate or replace tires."),
    ("Tires & Wheels", ["Bulge on tire sidewall", "Thumping noise from wheel"], "Damaged tire needs replacement", "Critical", "Replace the tire immediately; a blowout risk."),
    ("Tires & Wheels", ["Wobble from wheel", "Clicking from wheel area after a tire change"], "Loose wheel nuts", "Critical", "Stop and tighten the lug nuts to the specified torque."),
    ("Tires & Wheels", ["Visible rim damage", "Vibration after hitting a pothole"], "Bent wheel rim", "Medium", "Straighten or replace the rim."),

    # ---------------- 10. Electrical, Lights & AC ----------------
    ("Electrical, Lights & AC", ["Headlight is out", "Other lights work normally", "Bulb filament looks broken"], "Blown headlight bulb", "Low", "Replace the bulb."),
    ("Electrical, Lights & AC", ["Accessory is not working", "Fuse looks blackened or broken"], "Blown fuse", "Low", "Replace the fuse with one of the same amp rating."),
    ("Electrical, Lights & AC", ["AC blows warm air", "Compressor clutch cycles rapidly"], "Low AC refrigerant", "Low", "Find the leak and recharge the AC system."),
    ("Electrical, Lights & AC", ["AC blows warm air", "Loud noise when AC is on"], "Failing AC compressor", "Medium", "Replace the AC compressor and flush the system."),
    ("Electrical, Lights & AC", ["Weak airflow from vents", "Musty smell from AC", "Windows are slow to defog"], "Clogged cabin air filter", "Low", "Replace the cabin air filter."),
    ("Electrical, Lights & AC", ["Wipers streak or chatter", "Wiper blades are cracked"], "Worn wiper blades", "Low", "Replace the wiper blades."),
    ("Electrical, Lights & AC", ["Power window is stuck", "Grinding noise from door when pressing window switch"], "Faulty window regulator or motor", "Low", "Replace the window regulator or motor."),
    ("Electrical, Lights & AC", ["Key fob does not unlock the car", "Key fob battery has not been replaced recently"], "Dead key fob battery", "Low", "Replace the key fob battery (usually CR2032)."),
    ("Electrical, Lights & AC", ["Multiple electrical items work intermittently", "Lights flicker"], "Poor electrical ground connection", "Medium", "Clean and tighten the battery and chassis ground straps."),
    ("Electrical, Lights & AC", ["@Blown fuse", "Fuse blows again immediately"], "Short circuit in wiring", "High", "Do not use a larger fuse. Trace the short; see an auto electrician."),
]

RULES = [
    Rule(f"R{i:03d}", cat, conds, concl, sev, adv)
    for i, (cat, conds, concl, sev, adv) in enumerate(_RAW, start=1)
]

DIAGNOSES = sorted({r.conclusion for r in RULES})
SYMPTOMS = sorted({c for r in RULES for c in r.conditions if not c.startswith("@")})

# 300 assertions = symptoms + diagnoses, each with a stable ID
ASSERTIONS = {}
for _i, _s in enumerate(SYMPTOMS, start=1):
    ASSERTIONS[f"S{_i:03d}"] = _s
for _i, _d in enumerate(DIAGNOSES, start=1):
    ASSERTIONS[f"D{_i:03d}"] = _d

SYMPTOM_CATEGORY = {}
for _r in RULES:
    for _c in _r.conditions:
        if not _c.startswith("@"):
            SYMPTOM_CATEGORY.setdefault(_c, _r.category)

SEVERITY_ICON = {"Low": "🟢", "Medium": "🟡", "High": "🟠", "Critical": "🔴"}
