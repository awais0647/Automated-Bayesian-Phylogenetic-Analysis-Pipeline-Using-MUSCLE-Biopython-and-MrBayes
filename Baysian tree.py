import subprocess
from Bio import AlignIO

# ===============================
# Input and output file settings
# ===============================
input_fasta = "input.fasta.fas"   # your original fasta
aligned_fasta = "aligned.fasta"   # MUSCLE output
aligned_nexus = "aligned.nex"     # Nexus file with MrBayes block

# ===============================
# Step 1: Run MUSCLE alignment
# ===============================
print("🔹 Running MUSCLE alignment...")
subprocess.run(f"muscle -in {input_fasta} -out {aligned_fasta}", shell=True, check=True)

# ===============================
# Step 2: Convert alignment to NEXUS
# ===============================
print("🔹 Converting alignment to NEXUS...")
alignment = AlignIO.read(aligned_fasta, "fasta")

# Force Biopython to recognize sequences as DNA
for record in alignment:
    record.annotations["molecule_type"] = "DNA"
alignment.annotations["molecule_type"] = "DNA"

AlignIO.write(alignment, aligned_nexus, "nexus")

# ===============================
# Step 3: Append MrBayes block
# ===============================
print("🔹 Appending MrBayes block...")

with open(aligned_nexus, "a") as nex:
    nex.write("\n")  # ensure a newline before appending
    nex.write("""\
begin mrbayes;
   set autoclose=yes nowarn=yes;
   lset nst=6 rates=gamma;
   mcmc ngen=1000000 samplefreq=1000 nchains=4 printfreq=1000 diagnfreq=10000 burninfrac=0.25 savebrlens=yes;
   sump;
   sumt;
end;
""")

print(f"✅ Done! Created {aligned_nexus} with MrBayes block.")

# ===============================
# Step 4: Run MrBayes
# ===============================
print("🔹 Running MrBayes (this may take a while)...")
subprocess.run(f"mb {aligned_nexus}", shell=True, check=True)

print("🎉 Analysis complete! Check the .t files (trees) and .p files (parameters).")
