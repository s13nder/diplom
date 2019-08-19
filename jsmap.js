function map_fill(tableName)
{
	var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
				
				if(this.responseText == "-1") console.log("ERROR ON SERVER");
				else
				{
					var arr = JSON.parse(this.responseText);
					
					var data_obj = {};
					
					for(var i in arr)
					{
						var line = arr[i];
						data_obj[line["id"]] = new Array(line["quan_vacancy"], line["average_salary"], line["competition"]);
					}
					
					$('#vmap').vectorMap({
		    map: 'russia',
		    backgroundColor: '#ffffff',
			borderColor: '#ffffff',
			borderWidth: 2,
		    color: colorRegion,
			colors: highlighted_states,			
		    hoverOpacity: 0.7,		    
		    enableZoom: true,
		    showTooltip: true,			
			
			/// Отображаем объекты если они есть
			onLabelShow: function(event, label, code){
				name = '<p><font size="3" color="white"><strong>'+label.text()+'</strong><br> </p>';				
				if(data_obj[code]){
					list_obj = '<ul>';
					
					var columnIndex = 0;
					for(ob in data_obj[code])
					{		
						var dbValue = data_obj[code][ob];
						
						var displayValue = "нет данных";

						if(dbValue)
						{
							displayValue = dbValue;
						}

						list_obj += '<p><font size="3" color="white">'+ columnNames[columnIndex++] + displayValue +'</p>';
					}
					list_obj += '</ul>';
				}else{
					list_obj = '';
				}				
				label.html(name + list_obj);				
				list_obj = '';				
			},				
		});	
				
                	//console.log(parsedArr);
				}
            }
        };
		//xmlhttp.open("GET", "update_data.php", true);
		xmlhttp.open("GET", "update_data.php?table=" + tableName, true);
        xmlhttp.send();
}