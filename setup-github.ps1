<#=====================================================================
  setup-github.ps1
  Script automatique : installe Git + crée le dépôt GitHub
  et pousse le projet portfolio-aboubakar.
  
  Utilisation :
    1. Ouvre PowerShell en Administrateur
    2. cd "C:\Users\ABOU SERVICE\Downloads\portfolio-aboubakar"
    3. .\setup-github.ps1
=====================================================================#>

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  SETUP GITHUB - Portfolio Aboubakar" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# ── 1. Vérifier / Installer Git ──
$git = (Get-Command "git" -ErrorAction SilentlyContinue)
if (-not $git) {
    Write-Host "[...] Git non trouve. Installation en cours..." -ForegroundColor Yellow
    
    # Détecter l'architecture
    $arch = if ([Environment]::Is64BitOperatingSystem) { "x64" } else { "x86" }
    $url = "https://github.com/git-for-windows/git/releases/download/v2.48.1.windows.1/Git-2.48.1-64-bit.exe"
    $installer = "$env:TEMP\git-installer.exe"
    
    Write-Host "  Telechargement de Git $arch..." -ForegroundColor Gray
    try {
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        Invoke-WebRequest -Uri $url -OutFile $installer -UseBasicParsing
        Write-Host "  Telechargement termine." -ForegroundColor Green
    } catch {
        Write-Host "[!] Echec du telechargement. Installation manuelle requise." -ForegroundColor Red
        Write-Host "    Va sur https://git-scm.com/download/win et installe Git." -ForegroundColor Yellow
        Write-Host "    Puis relance ce script." -ForegroundColor Yellow
        exit 1
    }
    
    Write-Host "  Installation de Git (ne ferme pas cette fenetre)..." -ForegroundColor Gray
    $proc = Start-Process -FilePath $installer -ArgumentList "/VERYSILENT /NORESTART /NOCANCEL /SP- /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS /COMPONENTS=`"icons,ext,gitlfs,assoc,autoupdate`"" -Wait -PassThru
    if ($proc.ExitCode -ne 0) {
        Write-Host "[!] L'installation a echoue (code: $($proc.ExitCode))." -ForegroundColor Red
        Write-Host "    Installe Git manuellement depuis https://git-scm.com/download/win" -ForegroundColor Yellow
        exit 1
    }
    
    # Rafraichir PATH
    $env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [Environment]::GetEnvironmentVariable("Path", "User")
    $env:Path += ";C:\Program Files\Git\cmd"
    
    $git = (Get-Command "git" -ErrorAction SilentlyContinue)
    if (-not $git) {
        Write-Host "[!] Git installe mais pas dans le PATH." -ForegroundColor Red
        Write-Host "    Redemarre PowerShell en Administrateur puis relance ce script." -ForegroundColor Yellow
        exit 1
    }
    Write-Host "[OK] Git installe avec succes !" -ForegroundColor Green
} else {
    Write-Host "[OK] Git deja installe : $(git --version)" -ForegroundColor Green
}

# ── 2. Se placer dans le dossier du projet ──
$projectDir = "C:\Users\ABOU SERVICE\Downloads\portfolio-aboubakar"
if (-not (Test-Path $projectDir)) {
    Write-Host "[!] Dossier $projectDir introuvable." -ForegroundColor Red
    exit 1
}
Set-Location -Path $projectDir
Write-Host "[OK] Dossier : $projectDir" -ForegroundColor Green

# ── 3. Initialiser Git si pas deja fait ──
if (-not (Test-Path ".git")) {
    git init 2>&1 | Out-Null
    Write-Host "[OK] git init" -ForegroundColor Green
} else {
    Write-Host "[OK] Depot deja initialise" -ForegroundColor Green
}

# ── 4. Ajouter les fichiers et commiter ──
git add .
$status = git status --porcelain
if ($status) {
    git commit -m "Initial commit: portfolio STIMULATION CAISSE & CONNECT-PRO"
    Write-Host "[OK] Fichiers ajoutes et commit." -ForegroundColor Green
} else {
    Write-Host "[OK] Aucune modification a commiter." -ForegroundColor Green
}

# ── 5. Configurer la branche main ──
git branch -M main 2>&1 | Out-Null

# ── 6. Vérifier le remote ──
$remote = git remote -v
if (-not ($remote -match "origin")) {
    Write-Host ""
    Write-Host "=== CONNEXION A GITHUB ===" -ForegroundColor Cyan
    $repoName = "portfolio-aboubakar"
    $defaultUser = "AB-cloud-cyber"
    $user = Read-Host "Nom d'utilisateur GitHub [$defaultUser]"
    if (-not $user) { $user = $defaultUser }
    
    git remote add origin "https://github.com/$user/$repoName.git"
    Write-Host "[OK] Remote origin ajoute : https://github.com/$user/$repoName.git" -ForegroundColor Green
} else {
    Write-Host "[OK] Remote deja configure : $remote" -ForegroundColor Green
}

# ── 7. Push vers GitHub ──
Write-Host ""
Write-Host "=== PUSH VERS GITHUB ===" -ForegroundColor Cyan
Write-Host "Une fenetre de connexion GitHub va s'ouvrir." -ForegroundColor Yellow
Write-Host "Connecte-toi avec ton compte AB-cloud-cyber." -ForegroundColor Yellow
Write-Host ""

try {
    git push -u origin main 2>&1
    Write-Host ""
    Write-Host "[OK] Push reussi !" -ForegroundColor Green
    Write-Host "    https://github.com/AB-cloud-cyber/portfolio-aboubakar" -ForegroundColor Cyan
} catch {
    Write-Host ""
    Write-Host "[!] Echec du push." -ForegroundColor Red
    Write-Host "    Causes possibles :" -ForegroundColor Yellow
    Write-Host "      - Le depot n'existe pas encore sur GitHub" -ForegroundColor Yellow
    Write-Host "      - Identifiants incorrects" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "    Va sur https://github.com/new" -ForegroundColor White
    Write-Host "    Cree un depot nomme 'portfolio-aboubakar' (PUBLIC)" -ForegroundColor White
    Write-Host "    Puis relance ce script." -ForegroundColor White
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  TERMINE !" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
pause
