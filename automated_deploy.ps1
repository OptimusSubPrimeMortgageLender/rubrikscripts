
$nodename= "RVM183S035153.local"


# Payload to deploy Rubrik cluster
$json_payload = ‘
{  
	"name":"testcluster",
	"ntpServers":[  
	   "time.google.com"
	],
	"dnsNameservers":[  
	   "8.8.8.8",
	   "8.8.4.4"
	],
	"dnsSearchDomains":[  
 
	],
	"enableSoftwareEncryptionAtRest":true,
	"adminUserInfo":{  
	   "id":"admin",
	   "password":"RubrikGoForward",
	   "emailAddress":"dominic@rubrik.com"
	},
	"nodeConfigs":{  
	   "RVM183S035153":{  
		  "ipmiIpConfig":{  
			"netmask":"255.255.255.0",
			 "gateway":"10.0.2.1",
			 "address":"10.0.2.10"
		  },
		  "managementIpConfig":{  
			"netmask":"255.255.255.0",
			 "gateway":"10.0.1.1",
			 "address":"10.0.1.10"
		  }
	   },
	   "RVM183S035250":{  
		  "ipmiIpConfig":{  
			"netmask":"255.255.255.0",
			 "gateway":"10.0.2.1",
			 "address":"10.0.2.11"
		  },
		  "managementIpConfig":{  
			"netmask":"255.255.255.0",
			 "gateway":"10.0.1.1",
			 "address":"10.0.1.11"
		  }
	   },
	   "RVM183S035350":{  
		  "ipmiIpConfig":{  
			 "netmask":"255.255.255.0",
			 "gateway":"10.0.2.1",
			 "address":"10.0.2.12"
		  },
		  "managementIpConfig":{  
			"netmask":"255.255.255.0",
			 "gateway":"10.0.1.1",
			 "address":"10.0.1.12"
		  }
	   },
	   "RVM183S035644":{  
		  "ipmiIpConfig":{  
			"netmask":"255.255.255.0",
			 "gateway":"10.0.2.1",
			 "address":"10.0.2.13"
		  },
		  "managementIpConfig":{  
			"netmask":"255.255.255.0",
			 "gateway":"10.0.1.1",
			 "address":"10.0.1.13"
		  }
	   }
	}
 }‘

function update_bootstrap_status {
    $bootstatus = Invoke-WebRequest -SkipCertificateCheck  -Uri $("https://"+$nodename+"/api/internal/cluster/me/bootstrap?request_id="+$(($start_bootstrap.content | convertfrom-json).id)) -Method GET
    $bootstatus
}

$bootstrap_timer = 0

# Perform the deployment
$start_bootstrap = Invoke-WebRequest -SkipCertificateCheck -Uri $("https://"+$nodename+"/api/internal/cluster/me/bootstrap") -Method POST -Body $json_payload -TimeoutSec 6000 

# Grab the results of the deployment request
$bootstrap_status = update_bootstrap_status
write-host $bootstrap_status

while ($bootstrap_status -match 'IN_PROGRESS'){
    $bootstrap_status = update_bootstrap_status
    Clear-Host
    write-host -ForegroundColor Yellow "Bootstrap process has been running for" $bootstrap_timer.tostring() "seconds"
    $bootstrap_status.content | ConvertFrom-Json
    start-sleep -Seconds 10
    $bootstrap_timer = $bootstrap_timer + 10
}
if ($bootstrap_status -notmatch 'IN_PROGRESS'){
    write-host -ForegroundColor Green "Bootstrap process complete"
}

