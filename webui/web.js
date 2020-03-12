$(document).ready(function(){
  
    $("#searchfield").focus(function(){
        if($(this).val() == "Search contacts..."){
            $(this).val("");
        }
    });
    $("#searchfield").focusout(function(){
        if($(this).val() == ""){
            $(this).val("Search contacts...");
            
        }
    });
    
    $("#sendlove input").focus(function(){
        if($(this).val() == "Send Love..."){
            $(this).val("");
        }
    });
    $("#sendlove input").focusout(function(){
        if($(this).val() == ""){
            $(this).val("Send Love...");
            
        }
    });
        
    
    $(".record").each(function(){       
        $(this).click(function(){
            var childOffset = $(this).offset();
            var parentOffset = $(this).parent().parent().offset();
            var childTop = childOffset.top - parentOffset.top;
            var clone = $(this).find('img').eq(0).clone();
            var top = childTop+12+"px";
            
            $(clone).css({'top': top}).addClass("floatingImg").appendTo("#chatbox");                                    
            
            setTimeout(function(){$("#title p").addClass("animate");$("#title").addClass("animate");}, 100);
            setTimeout(function(){
                $("#chat-messages").addClass("animate");
                $('.cx, .cy').addClass('s1');
                setTimeout(function(){$('.cx, .cy').addClass('s2');}, 100);
                setTimeout(function(){$('.cx, .cy').addClass('s3');}, 200);         
            }, 150);                                                        
            
            $('.floatingImg').animate({
                'width': "68px",
                'left':'108px',
                'top':'20px'
            }, 200);
            
            var name = $(this).find("p strong").html();
            var email = $(this).find("p span").html();                                                      
            $("#title p").html(name);
            $("#title span").html(email);         
            
            $(".message").not(".right").find("img").attr("src", $(clone).attr("src"));                                  
            $('#recordslist').fadeOut();
            $('#messageview').fadeIn();
        
            
            $('#close').unbind("click").click(function(){               
                $("#chat-messages, #title, #title p").removeClass("animate");
                $('.cx, .cy').removeClass("s1 s2 s3");
                $('.floatingImg').animate({
                    'width': "40px",
                    'top':top,
                    'left': '12px'
                }, 200, function(){$('.floatingImg').remove()});                
                
                setTimeout(function(){
                    $('#messageview').fadeOut();
                    $('#recordslist').fadeIn();             
                }, 50);
            });
            
        });
    });         
});