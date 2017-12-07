from functools import wraps
from time import sleep
import threading
import shutil


class FuzzManager:
	def __init__(self):
                self.mutatemode = None # radamsa windows binary/docker container
		self.samplePath = "sample"
		self.mutatePath = "testcase"
		self.crashPath = "crash"
		self.targetPath = "C:\\Program Files\\VUPlayer\\VUPlayer.exe"		
		self.loop = 10000
		self.testNumber = 0
		self.pid = None

        def mutate(self):
                print "mutate"
                if self.mutatemode == "binary":
                    print "/bin/radamsa.exe -r sample -n "+ self.loop +" -o testcase/%n"
                elif self.mutatemode == "docker":
                    print "docker run -d -v []:/testcase,[]:/sample --name=radamsa bongbongco88/radamsa"
                        
	def execute(self):
		print "target Execute"	
		print(self.targetPath, self.mutatePath + "/" + str(self.testNumber)) 
		
	def debug(self):
		print "target Debug"
		self.waitingForProcess()

	def checkingCount(func): 
		@wraps(func)
		def wrapper(self, *args, **kwargs):
			if self.testNumber > self.loop:
				print "Completed Fuzzing Test"
				exit()
			self.testNumber = self.testNumber + 1	
			print "TestCase: ", self.testNumber	
			return func(self, *args, **kwargs) 
		return wrapper

	@checkingCount
	def fuzz(self):
		fuzzThread = threading.Thread(target=self.execute)	
		fuzzThread.setDaemon(0)
		fuzzThread.start()
	
		self.waitingForProcess()

		monitoringThread = threading.Thread(target=self.debug)
		monitoringThread.setDaemon(0)
		monitoringThread.start()

	def caseCopy(self):
		print(self.mutatePath+'/'+str(self.testNumber), str(self.testNumber)+'/'+self.crashPath)
		shutil.copy(self.mutatePath+'/'+str(self.testNumber), str(self.testNumber)+'/'+self.crashPath)
	
	def waitingForProcess(self):
		counter = 0
		while self.pid == None:
			if counter < 5:
				sleep(1)
				counter = counter + 1
				if counter >= 5:
                                    break
        
        def setMutateMode(self, mode):
                self.mutatemode = mode

	def start(self):
                self.mutate()
		while True:
			self.fuzz()	


def main():
	fuzzManager = FuzzManager()
	fuzzManager.start()

if __name__ == "__main__":
	main()
