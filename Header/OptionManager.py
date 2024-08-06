import json

class SaveDataManager:
    def __init__(self):
        self._CONFIG = self.InitConfig()
        self._DEFALUT_MAX = 200
        self._DEFALUT_MIN = 20

    def CheckValidRange(self):
        if self._CONFIG['max_value'] < self._CONFIG['min_value']:
            self._CONFIG['max_value'] = self._DEFALUT_MAX
            self._CONFIG['min_value'] = self._DEFALUT_MIN
        self.SaveConfig()

    def InitConfig(self):
        with open("./Header/log.json", 'r') as File:
            return json.load(File)
    
    def SetOption(self, key, value):
        self._CONFIG[key] = value
    
    def SaveConfig(self):
        _CHANGED_LOG = self._CONFIG
        with open("./Header/log.json", 'w') as File:
            json.dump(_CHANGED_LOG, File, indent=4)

# Option Class
_LOG = SaveDataManager()