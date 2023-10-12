import cx_Freeze

executables = [cx_Freeze.Executable('CyberRace.py')]

cx_Freeze.setup(
    name="Cyber Race",
    options={'build_exe': {'packages':['pygame'],
                           'include_files':['css']}},

    executables = executables
    
)