import pyotp
import time 

#totp = pyotp.TOTP("JBSWY3DPEHPK3PXP")
#otp=totp.now()
#print("Current OTP:", otp)


totp = pyotp.TOTP('base32secret3232')
print(totp.now()) # => '492039'
otp=totp.now()
print(otp)
# OTP verified for current time
res=totp.verify(otp) # => True
print(res)
time.sleep(30)
print(totp.now())
res=totp.verify(otp) # => False
print(res)