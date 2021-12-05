import os
import traceback
from time import sleep
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC

print('初始化浏览器')
USERNAME   = os.environ['ID']
PASSWORD   = os.environ['PASSWORD']
LOCATION   = os.environ['LOCATION']
ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Mobile/14A403 NetType/WIFI Language/zh_CN'
app = 'HuaWei-AnyOffice/1.0.0/cn.edu.hit.welink'
option = webdriver.ChromeOptions()
option.headless = True
option.add_argument('user-agent='+ua)
driver = webdriver.Chrome(executable_path= '/usr/bin/chromedriver', options = option)

print('正在上报')
driver.get('https://ids.hit.edu.cn/authserver/')
driver.find_element_by_id('mobileUsername').send_keys(USERNAME)
driver.find_element_by_id('mobilePassword').send_keys(PASSWORD)
driver.find_element_by_id('load').click()

driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": ua + ' ' + app})

success = False
for i in range (0, 5):
	try:
		driver.get('https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsMrsbNew/edit')
		driver.execute_script(f'kzl10 = "{LOCATION}"')
		driver.execute_script('document.getElementById("kzl18-0").checked = true')
		driver.execute_script('document.getElementById("kzl32-2").checked = true')
		try:
			driver.execute_script('document.getElementById("txfscheckbox").click()')
		except:
			pass
		try:
			# 如果有多的按钮，按，没多的按钮就算了
			driver.execute_script('document.getElementById("txfscheckbox1").click()')
			driver.execute_script('document.getElementById("txfscheckbox2").click()')
		except:
			pass
		try:
			driver.execute_script('document.getElementById("txfscheckbox3").click()') # ……变成3个按钮了……
		except:
			pass
		driver.find_element_by_class_name('submit').click()
		success = True
		break
	except:
		traceback.print_exc()
		print('失败' + str(i+1) + '次，正在重试...')
driver.quit()
if success:
	print('上报完成')
else:
	raise Exception('上报多次失败，可能学工系统已更新')
