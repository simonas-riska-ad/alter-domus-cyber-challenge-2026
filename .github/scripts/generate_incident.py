from pathlib import Path
import csv, random, zipfile, shutil
from datetime import datetime, timedelta

build = Path("tmp_incident_build")
if build.exists():
    shutil.rmtree(build)
build.mkdir(parents=True)

outdir = Path("docs/files/reconstruct-the-incident")
outdir.mkdir(parents=True, exist_ok=True)
zip_path = outdir / "Northstar_Incident_Reconstruction.zip"

rng = random.Random(19092026)
victim = "maria.keller"
attacker_ip = "203.0.113.146"
vpn_ip = "10.44.7.23"
target_file = "investor_distributions_q3.csv"

base = datetime(2026, 9, 22, 7, 0, 0)
users = ["alex.morgan","julia.meyer","nina.patel","thomas.lee","sophie.bernard","marco.rossi","maria.keller"]
normal_ips = {
    "alex.morgan":"198.51.100.21",
    "julia.meyer":"198.51.100.34",
    "nina.patel":"198.51.100.48",
    "thomas.lee":"198.51.100.52",
    "sophie.bernard":"198.51.100.71",
    "marco.rossi":"198.51.100.63",
    "maria.keller":"198.51.100.84",
}

auth = []
for _ in range(130):
    ts = base + timedelta(seconds=rng.randint(0, 13*3600))
    user = rng.choice(users)
    status = rng.choices(["SUCCESS","FAIL"], weights=[96,4])[0]
    detail = "mfa_ok" if status == "SUCCESS" else "bad_password"
    auth.append(f"{ts.isoformat()}Z auth user={user} source_ip={normal_ips[user]} result={status} detail={detail}")
auth += [
    "2026-09-22T22:13:51Z auth user=maria.keller source_ip=203.0.113.146 result=FAIL detail=bad_password",
    "2026-09-22T22:14:12Z auth user=maria.keller source_ip=203.0.113.146 result=FAIL detail=bad_password",
    "2026-09-22T22:14:36Z auth user=maria.keller source_ip=203.0.113.146 result=SUCCESS detail=mfa_push_approved",
]
(build/"authentication.log").write_text("\n".join(sorted(auth))+"\n", encoding="utf-8")

vpn = []
for _ in range(90):
    user = rng.choice(users)
    start = base + timedelta(seconds=rng.randint(0, 12*3600))
    end = start + timedelta(seconds=rng.randint(300,7200))
    vpn.append([start.isoformat()+"Z", end.isoformat()+"Z", user, normal_ips[user], f"10.44.{rng.randint(1,6)}.{rng.randint(10,240)}", "client", "normal"])
vpn.append(["2026-09-22T22:15:02Z","2026-09-22T22:31:44Z",victim,attacker_ip,vpn_ip,"client","new_device"])
vpn.sort(key=lambda r:r[0])
with (build/"vpn_sessions.csv").open("w", newline="", encoding="utf-8") as f:
    w=csv.writer(f)
    w.writerow(["session_start_utc","session_end_utc","user","source_ip","assigned_ip","client_type","device_note"])
    w.writerows(vpn)

portal = []
for _ in range(170):
    ts = base + timedelta(seconds=rng.randint(0, 13*3600))
    user = rng.choice(users)
    src = f"10.44.{rng.randint(1,6)}.{rng.randint(10,240)}"
    path = rng.choice(["/portal/home","/documents","/documents/q3-report.pdf","/investors/overview","/capital-activity","/notifications"])
    status = rng.choices([200,304,403], weights=[88,9,3])[0]
    portal.append(f"{ts.isoformat()}Z user={user} src={src} method=GET path={path} status={status} bytes={rng.randint(400,120000)}")
portal += [
    "2026-09-22T22:16:11Z user=maria.keller src=10.44.7.23 method=GET path=/portal/home status=200 bytes=3184",
    "2026-09-22T22:17:05Z user=maria.keller src=10.44.7.23 method=GET path=/investors/overview status=200 bytes=9412",
    "2026-09-22T22:18:42Z user=maria.keller src=10.44.7.23 method=GET path=/exports status=200 bytes=6110",
    "2026-09-22T22:19:07Z user=maria.keller src=10.44.7.23 method=GET path=/exports/investor_distributions_q3.csv status=200 bytes=284771",
]
(build/"portal_access.log").write_text("\n".join(sorted(portal))+"\n", encoding="utf-8")

events = []
for _ in range(120):
    ts = base + timedelta(seconds=rng.randint(0, 13*3600))
    user = rng.choice(users)
    events.append([ts.isoformat()+"Z",f"WS-{rng.randint(101,145)}",user,rng.choice(["browser_start","document_open","file_save","teams_message","browser_download"]),rng.choice(["q3-report.pdf","meeting-notes.docx","reconciliation.xlsx","portal.northstar.example","none"]),"normal"])
events += [
    ["2026-09-22T22:15:19Z","BYOD-UNKNOWN",victim,"browser_start","portal.northstar.example","unmanaged"],
    ["2026-09-22T22:19:09Z","BYOD-UNKNOWN",victim,"browser_download",target_file,"unmanaged"],
    ["2026-09-22T22:20:02Z","BYOD-UNKNOWN",victim,"file_save",target_file,"unmanaged"],
]
events.sort(key=lambda r:r[0])
with (build/"endpoint_events.csv").open("w", newline="", encoding="utf-8") as f:
    w=csv.writer(f)
    w.writerow(["timestamp_utc","device","user","event_type","detail","device_state"])
    w.writerows(events)

(build/"README.txt").write_text(
    "NORTHSTAR - INCIDENT RECONSTRUCTION PACKAGE\n\n"
    "A fictional security team collected four data sources after suspicious activity was reported:\n\n"
    "- authentication.log\n- vpn_sessions.csv\n- portal_access.log\n- endpoint_events.csv\n\n"
    "Reconstruct the incident and identify:\n"
    "1. the affected user\n2. the external source IP used for the unauthorized access\n3. the sensitive file that was downloaded\n\n"
    "Submit the flag as:\nADCTF{username_ip_filename}\n\n"
    "Example:\nADCTF{alex.morgan_192.0.2.10_example.csv}\n\n"
    "All identities, addresses, systems and records in this package are synthetic.\n",
    encoding="utf-8"
)

if zip_path.exists():
    zip_path.unlink()
with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for n in ["README.txt","authentication.log","vpn_sessions.csv","portal_access.log","endpoint_events.csv"]:
        z.write(build/n, arcname=n)

with zipfile.ZipFile(zip_path,"r") as z:
    assert z.testzip() is None
    joined=b"\n".join(z.read(n) for n in z.namelist())
    assert b"maria.keller" in joined
    assert b"203.0.113.146" in joined
    assert b"investor_distributions_q3.csv" in joined
    print(z.namelist())
    print(zip_path.stat().st_size)
