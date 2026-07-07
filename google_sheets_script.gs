/**
 * Google Apps Script Web App for Logging Searches
 * 
 * Instructions:
 * 1. Open your Google Sheet.
 * 2. Click on 'Extensions' -> 'Apps Script'.
 * 3. Delete any default code and paste this script.
 * 4. Click 'Save' (floppy disk icon).
 * 5. Click 'Deploy' -> 'New deployment'.
 * 6. Select type 'Web app'.
 * 7. Set 'Execute as' to 'Me'.
 * 8. Set 'Who has access' to 'Anyone'.
 * 9. Click 'Deploy', authorize the permissions, and copy the Web App URL.
 */

function doPost(e) {
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    
    // 1. Add headers if the sheet is empty (First run auto-setup)
    if (sheet.getLastRow() === 0) {
      var headers = [
        "תאריך ושעה", 
        "מזהה מכשיר", 
        "קלט חיפוש", 
        "כותרת מאמר רשמית", 
        "מזהה DOI", 
        "סטטוס תוצאה", 
        "קישור שהורד/נמצא"
      ];
      sheet.appendRow(headers);
      
      // Design headers with premium dark slate background and white bold text
      var headerRange = sheet.getRange(1, 1, 1, headers.length);
      headerRange.setFontWeight("bold");
      headerRange.setBackground("#0F172A"); // Modern slate dark theme
      headerRange.setFontColor("#FFFFFF");
      headerRange.setHorizontalAlignment("right");
      sheet.setFrozenRows(1);
      
      // Adjust column widths automatically
      for (var col = 1; col <= headers.length; col++) {
        sheet.autoResizeColumn(col);
      }
    }
    
    // 2. Parse payload data
    var data = JSON.parse(e.postData.contents);
    
    var timestamp = new Date();
    var userId = data.userId || "Local User";
    var query = data.query || "N/A";
    var resolvedTitle = data.resolvedTitle || "N/A";
    var doi = data.doi || "N/A";
    var status = data.status || "N/A";
    var linkFound = data.linkFound || "N/A";
    
    // 3. Append search log row
    sheet.appendRow([
      timestamp, 
      userId, 
      query, 
      resolvedTitle, 
      doi, 
      status, 
      linkFound
    ]);
    
    // Format alignment to RTL/Right for Hebrew users
    var lastRow = sheet.getLastRow();
    sheet.getRange(lastRow, 1, 1, 7).setHorizontalAlignment("right");
    
    // Auto-fit columns to content size
    for (var col = 1; col <= 7; col++) {
      sheet.autoResizeColumn(col);
    }
    
    return ContentService.createTextOutput(JSON.stringify({ status: "success" }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({ status: "error", message: error.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
