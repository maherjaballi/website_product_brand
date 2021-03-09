$(document).ready(function(){ 
	if($('.clear-brand-filter')){
		$(".clear-brand-filter").click(function(){
			var self=$(this)
			var curent_div = $(self).next("ul");
			
			$(curent_div).find("input:checked").each(function(){
				$(this).removeAttr("checked");
			});
			$("form.js_attributes input").closest("form").submit();
		});
	}
	if($('.clear-attrib-filter')){
		$(".clear-attrib-filter").click(function(e){
			var target = $(e.target)
            if(target.parent().next('.nav-stacked').length){
                target.parent().next('.nav-stacked').find("input:checked").each(function(){
                    $(this).removeAttr("checked");
                });
                $("form.js_attributes input").closest("form").submit();
            }else{
                target.parents().find('label').find("input:checked").each(function(){
                    $(this).removeAttr("checked");
                });
                $("form.js_attributes input").closest("form").submit();
            }
		});
	}
	$(".as_our_brand").owlCarousel({
        items: 5,
        margin: 10,
        nav: true,
        pagination: false,
        responsive: {
            0: {
                items: 2,
            },
            481: {
                items: 2,
            },
            768: {
                items: 4,
            },
            1024: {
                items: 6,
            }
        }

    });
});

