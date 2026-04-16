import sys

# -------------------------------------------------
# Instellingen
# -------------------------------------------------
VERBRUIK_KM_PER_LITER = 11.0
MIN_TANK_LITERS = 5.0
MAX_TANK_LITERS = 50.0

# Verwachte liters via command-line parameter
verwachte_liters = None
if len(sys.argv) > 1:
    try:
        verwachte_liters = float(sys.argv[1])
    except ValueError:
        pass

# Stations: afstand (km vanaf huis) -> (prijs €/L, naam)
stations = {
    1.1: (2.249, "Avia Hengelosestraat 176"),
    1.6: (2.239, "TinQ Hengelosestraat 12"),
    11.6: (2.147, "TinQ Breemarsweg 411"),
    12.2: (2.014, "Hauptstraße 8, Ammeloe"),
    13.5: (1.979, "Shell Haaksbergener Str. 18 Ahaus"),
    14.2: (1.975, "KK Gronauer Str. 30 Ahaus"),
    27.6: (1.969, "Markant Nienborger Str. Gronau")
}

# -------------------------------------------------
# Hulpfunctie
# -------------------------------------------------
def bereken_rendabiliteit(extra_afstand_km, prijs_verder, prijs_ref):
    """
    extra_afstand_km = extra enkele reis afstand t.o.v. referentie
    """
    extra_km = 2 * extra_afstand_km
    extra_liters = extra_km / VERBRUIK_KM_PER_LITER
    kosten_extra = extra_liters * prijs_verder
    prijsverschil = prijs_ref - prijs_verder

    if prijsverschil <= 0:
        return None, extra_km, extra_liters, kosten_extra

    min_liters = kosten_extra / prijsverschil

    if not MIN_TANK_LITERS <= min_liters <= MAX_TANK_LITERS:
        return None, extra_km, extra_liters, kosten_extra

    return min_liters, extra_km, extra_liters, kosten_extra

# -------------------------------------------------
# Referentiestation
# -------------------------------------------------
ref_afstand = min(stations.keys())
ref_prijs, ref_naam = stations[ref_afstand]

print(f"REFERENTIE: {ref_naam} ({ref_afstand:.1f} km) — €{ref_prijs:.3f}/L")
print(f"Verbruik: {VERBRUIK_KM_PER_LITER} km/L")
print(f"Tanklimiet: {MIN_TANK_LITERS} – {MAX_TANK_LITERS} L")
if verwachte_liters:
    print(f"Verwachte tankbeurt: {verwachte_liters:.1f} L")

print("=" * 166)

# -------------------------------------------------
# Tabelheader
# -------------------------------------------------
header = (
    f"{'Naam':<35}"
    f"{'Afst(km)':>9}"
    f"{'€/L':>8}"
    f"{'Extra km':>10}"
    f"{'Extra L':>9}"
    f"{'Min. L':>9}"
    f"{'Prijs bij min (€)':>18}"
)

if verwachte_liters:
    header += (
        f"{f'Bij {verwachte_liters:.0f}L rendabel?':>24}"
        f"{f'Prijs bij {verwachte_liters:.0f}L (€)':>22}"
        f"{'Netto besparing (€)':>22}"
    )

print(header)
print("-" * 166)

# -------------------------------------------------
# Referentieregel
# -------------------------------------------------
ref_row = (
    f"{ref_naam:<35}"
    f"{ref_afstand:9.1f}"
    f"{ref_prijs:8.3f}"
    f"{0:10.1f}"
    f"{0:9.2f}"
    f"{'ref':>9}"
    f"{ref_prijs * MIN_TANK_LITERS:18.2f}"
)
if verwachte_liters:
    tot_prijs_ref = verwachte_liters * ref_prijs
    ref_row += f"{'ref':>24}{tot_prijs_ref:22.2f}{0:22.2f}"


print(ref_row)

# -------------------------------------------------
# Overige stations
# -------------------------------------------------
for afstand, (prijs, naam) in sorted(stations.items()):
    if afstand == ref_afstand:
        continue

    extra_afstand = max(0.0, afstand - ref_afstand)
    min_liters, extra_km, extra_liters, kosten_extra = bereken_rendabiliteit(
        extra_afstand, prijs, ref_prijs
    )

    if min_liters is None:
        min_txt = "-"
        prijs_min = "-"
    else:
        min_txt = f"{min_liters:.1f}"
        prijs_min = f"{min_liters * prijs:.2f}"

    row = (
        f"{naam:<35}"
        f"{afstand:9.1f}"
        f"{prijs:8.3f}"
        f"{extra_km:10.1f}"
        f"{extra_liters:9.2f}"
        f"{min_txt:>9}"
        f"{prijs_min:>18}"
    )

    if verwachte_liters:
        prijsverschil = ref_prijs - prijs
        netto = (
            verwachte_liters * prijsverschil - kosten_extra
            if prijsverschil > 0
            else -kosten_extra
        )
        rendabel = "JA" if min_liters and verwachte_liters >= min_liters else "NEE"
        tot_prijs = verwachte_liters * prijs
        row += f"{rendabel:>24}{tot_prijs:22.2f}{netto:22.2f}"

    print(row)

print("=" * 166)
